import requests
import json
from config import PPLX_API_KEY, PPLX_API_URL

class PerplexityClient:
    def __init__(self):
        self.api_key = PPLX_API_KEY
        self.base_url = PPLX_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_content(self, prompt, platform, original_content=""):
        """Generate platform-optimized content using Perplexity API"""
        
        system_prompt = self._get_system_prompt(platform)
        user_prompt = self._get_user_prompt(platform, original_content, prompt)
        
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",  # ✅ CORRECTED MODEL
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "top_p": 0.9,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request Error: {str(e)}"
        except KeyError as e:
            return f"Unexpected API response format: {str(e)}"
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def _get_system_prompt(self, platform):
        """Get system prompt based on platform"""
        prompts = {
            "twitter": """You are a social media expert specializing in Twitter content. Create engaging, concise tweets that maximize impact within character limits. Use appropriate hashtags and maintain a conversational tone.""",
            "linkedin": """You are a professional content creator for LinkedIn. Create insightful, professional posts that add value to business conversations. Maintain a formal yet engaging tone.""",
            "newsletter": """You are an email newsletter specialist. Create compelling newsletter content with clear structure, engaging subject lines, and valuable insights for readers."""
        }
        return prompts.get(platform, "Create engaging content for the specified platform.")
    
    def _get_user_prompt(self, platform, original_content, additional_prompt):
        """Generate user prompt for the API"""
        base_prompt = f"""
Create optimized content for {platform.upper()} based on the following:

ORIGINAL CONTENT:
{original_content}

ADDITIONAL INSTRUCTIONS:
{additional_prompt}

Return only the final optimized content without any explanations.
"""
        return base_prompt.strip()