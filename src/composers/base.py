from abc import ABC, abstractmethod
from typing import Dict

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