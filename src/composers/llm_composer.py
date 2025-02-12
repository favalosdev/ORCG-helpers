import json
import google.generativeai as genai

from src.config.settings import COMPOSITION_PROMPT_PATH
from src.utils.safety_context import SafetyContext
from src.composers.base import BaseComposer

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
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def save_markdown(self, content: str, output_path: str):
        with open(output_path, 'w') as file:
            file.write(content) 