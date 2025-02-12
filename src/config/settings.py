import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
API_KEY = os.getenv('GEMINI_API_KEY')

# File paths
EXTRACTION_PROMPT_PATH = "data/prompts/extraction-prompt.md"
COMPOSITION_PROMPT_PATH = "data/prompts/composition-prompt.md"
EXISTING_MD_PATH = "data/report/current_report.md"
OUTPUT_MD_PATH = "data/report/updated_report.md"

# Constants
SIMILARITY_THRESHOLD = 0.9 