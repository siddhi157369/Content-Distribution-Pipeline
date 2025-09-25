import os
from dotenv import load_dotenv

load_dotenv()

# Perplexity API Configuration
PPLX_API_KEY = os.getenv("PPLX_API_KEY", "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")
PPLX_API_URL = "https://api.perplexity.ai/chat/completions"

# Platform-specific configurations
PLATFORM_CONFIG = {
    "twitter": {
        "max_length": 280,
        "thread_max": 25,
        "hashtag_recommendation": True
    },
    "linkedin": {
        "max_length": 3000,
        "professional_tone": True,
        "hashtag_recommendation": True
    },
    "newsletter": {
        "max_length": 5000,
        "include_subject": True,
        "formal_tone": True
    }
}