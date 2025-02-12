import os
from dotenv import load_dotenv
import json
from typing import List, Dict, Protocol
import PyPDF2
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from datetime import datetime
from pydantic import BaseModel, Field, validator

load_dotenv()

# Constants
API_KEY = os.getenv('GEMINI_API_KEY')

'''
PDF_PATH = "data/evaluations/security_eval.pdf"
EXISTING_MD_PATH = "data/markdown/current_report.md"
OUTPUT_MD_PATH = "data/markdown/updated_report.md"
'''

EXTRACTION_PROMPT_PATH = "data/prompts/extraction-prompt.md"
COMPOSITION_PROMPT_PATH = "data/prompts/composition-prompt.md"
EXISTING_MD_PATH = "data/report/current_report.md"
OUTPUT_MD_PATH = "data/report/updated_report.md"


# PDF_PATH = "data/evals/o3-mini-system-card-feb10.pdf"

SIMILARITY_THRESHOLD = 0.9

# os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
# os.makedirs(os.path.dirname(OUTPUT_MD_PATH), exist_ok=True)

class SafetyContext:
    ACADEMIC_HEADER = """
    ACADEMIC RESEARCH CONTEXT:
    - Research Institution: Observatorios de Riesgos Catastróficos Globales (ORCG)
    - Website: orcg.info
    - Research Purpose: Academic analysis of AI capabilities for policy recommendations
    - Project Goal: Inform policymakers about AI safety measures and capabilities
    - Research Ethics: This analysis is conducted under academic oversight for policy research
    """

class BaseExtractor(ABC):
    @abstractmethod
    def read_pdf(self, pdf_path: str) -> str:
        pass

    @abstractmethod
    def extract_information(self, text: str) -> Dict:
        pass

    '''
    @abstractmethod
    def validate_extraction(self, text: str, runs: int = 3) -> Dict:
        pass
    '''

class BaseComposer(ABC):
    @abstractmethod
    def read_markdown(self, md_path: str) -> str:
        pass
            
    @abstractmethod
    def compose_updated_markdown(self, original_md: str, new_info: Dict) -> str:
        pass
    
    @abstractmethod
    def save_markdown(self, content: str, output_path: str):
        pass

class MetricModel(BaseModel):
    type: str = Field(..., regex='^(QUANTITATIVE|QUALITATIVE)$')
    value: str
    unit: Optional[str] = None

class PerformanceModel(BaseModel):
    score: Union[float, str]
    baseline: Optional[str] = None
    comparison: Optional[str] = None

class ContextModel(BaseModel):
    test_conditions: str
    limitations: List[str]
    assumptions: List[str]

class SourceInfoModel(BaseModel):
    section: str
    page: Optional[int] = None
    confidence: str = Field(..., regex='^(HIGH|MEDIUM|LOW)$')

class EvidenceItemModel(BaseModel):
    category: str = Field(..., regex='^(INTELLIGENCE_GATHERING|SOCIAL_MANIPULATION|ATTACK_TOOL_DEVELOPMENT|SYSTEM_INFILTRATION|ATTACK_ORCHESTRATION)$')
    llm_family: str = Field(..., regex='^(CLAUDE|GPT|GEMINI|OTHER)$')
    capability: str
    metric: MetricModel
    performance: PerformanceModel
    context: ContextModel
    source_info: SourceInfoModel

class CoverageGapModel(BaseModel):
    category: str
    reason: str

class ConfidenceSummaryModel(BaseModel):
    overall_score: str = Field(..., regex='^(HIGH|MEDIUM|LOW)$')
    methodology_strength: str = Field(..., regex='^(HIGH|MEDIUM|LOW)$')
    data_quality: str = Field(..., regex='^(HIGH|MEDIUM|LOW)$')

class MetadataModel(BaseModel):
    total_evidence_points: int
    coverage_gaps: List[CoverageGapModel]
    confidence_summary: ConfidenceSummaryModel
    extraction_timestamp: str

    @validator('extraction_timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Invalid ISO 8601 timestamp')

class ExtractionResponseModel(BaseModel):
    evidence_items: List[EvidenceItemModel]
    metadata: MetadataModel

class LLMExtractor(BaseExtractor):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        
        with open(EXTRACTION_PROMPT_PATH, 'r') as f:
            self.prompt_template = f"{SafetyContext.ACADEMIC_HEADER}\n{f.read()}"

    def read_pdf(self, pdf_path: str) -> str:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return " ".join(page.extract_text() for page in reader.pages)

    def extract_information(self, text: str) -> Dict:
        prompt = f"{self.prompt_template}\n{text}"
        response = self.model.generate_content(prompt)
        
        try:
            # Parse the raw JSON response
            raw_data = json.loads(response.text)
            
            # Validate against our schema
            validated_data = ExtractionResponseModel(**raw_data)
            
            # Add timestamp if missing
            if 'extraction_timestamp' not in raw_data['metadata']:
                raw_data['metadata']['extraction_timestamp'] = datetime.utcnow().isoformat()
            
            return raw_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Schema validation error: {str(e)}")

class LLMComposer(BaseComposer):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        with open(COMPOSITION_PROMPT_PATH, 'r') as f:
            self.prompt_template = f"{SafetyContext.ACADEMIC_HEADER}\n{f.read()}"
    
    def read_markdown(self, md_path: str) -> str:
        with open(md_path, 'r') as file:
            return file.read()
            
    def compose_updated_markdown(self, original_md: str, new_info: Dict) -> str:
        prompt = self.prompt_template.format(
            original_md=original_md,
            new_info=json.dumps(new_info, indent=2)
        )
        
        response = self.model.generate_content(prompt.format(
            original_md=original_md,
            new_info=json.dumps(new_info, indent=2)
        ))

        return response.text
    
    def save_markdown(self, content: str, output_path: str):
        with open(output_path, 'w') as file:
            file.write(content)

def process_evaluation(
    pdf_path: str,
    existing_md_path: str,
    output_md_path: str,
    extractor: BaseExtractor,
    composer: BaseComposer
) -> Dict:
    # Read PDF text to evaluate
    pdf_text = extractor.read_pdf(pdf_path)
    extraction = extractor.extract_information(pdf_text)

    for evidence in extraction["evidence_items"]:
        print(evidence)
    
    '''
    original_md = composer.read_markdown(existing_md_path)

    validated_info = extractor.validate_extraction(pdf_text)
    
    if not validated_info.get("validated", False):
        raise ValueError("Information extraction could not be validated")
    
    original_md = composer.read_markdown(existing_md_path)
    '''

    '''
    updated_md = composer.compose_updated_markdown(original_md, validated_info["extraction"])
    composer.save_markdown(updated_md, output_md_path)
    
    return {
        "status": "success",
        "confidence": validated_info["confidence"],
        "output_path": output_md_path
    }
    '''

    return { "status": "success" }
    
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process PDF evaluation documents")
    parser.add_argument("--pdf_path", type=str, help="Path to the PDF evaluation document")
    args = parser.parse_args()

    if not API_KEY:
        raise ValueError("API_KEY not found in environment variables")
    
    extractor = LLMExtractor(API_KEY)
    composer = LLMComposer(API_KEY)
        
    result = process_evaluation(
        pdf_path=args.pdf_path,
        existing_md_path=EXISTING_MD_PATH,
        output_md_path=OUTPUT_MD_PATH,
        extractor=extractor,
        composer=composer
    )

    # print(json.dumps(result, indent=2))