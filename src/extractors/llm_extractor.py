import json
from datetime import datetime
import PyPDF2
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from typing import Dict

from src.config.settings import EXTRACTION_PROMPT_PATH
from src.utils.safety_context import SafetyContext
from src.extractors.base import BaseExtractor

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
            raw_data = json.loads(response.text)
            
            if 'extraction_timestamp' not in raw_data['metadata']:
                raw_data['metadata']['extraction_timestamp'] = datetime.now(datetime.UTC).isoformat()
            
            return raw_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Schema validation error: {str(e)}") 