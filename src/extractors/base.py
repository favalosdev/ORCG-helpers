from abc import ABC, abstractmethod
from typing import Dict

class BaseExtractor(ABC):
    @abstractmethod
    def read_pdf(self, pdf_path: str) -> str:
        pass

    @abstractmethod
    def extract_information(self, text: str) -> Dict:
        pass 