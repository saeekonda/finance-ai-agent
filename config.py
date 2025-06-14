import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Optional: Print warnings if keys are missing (helpful during development)
if not ALPHA_VANTAGE_API_KEY:
    print("Warning: ALPHA_VANTAGE_API_KEY not found in .env. Some features may not work.")
if not FMP_API_KEY:
    print("Warning: FMP_API_KEY not found in .env. Some features may not work.")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in .env. AI summarization will not work.")
if not NEWS_API_KEY:
    print("Warning: NEWS_API_KEY not found in .env. News fetching will not work.")