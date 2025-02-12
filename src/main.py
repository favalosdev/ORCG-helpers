import argparse
from typing import Dict

from src.config.settings import API_KEY, EXISTING_MD_PATH, OUTPUT_MD_PATH
from src.extractors.llm_extractor import LLMExtractor
from src.composers.llm_composer import LLMComposer

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
    
    return {"status": "success"}

def main():
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

if __name__ == "__main__":
    main() 