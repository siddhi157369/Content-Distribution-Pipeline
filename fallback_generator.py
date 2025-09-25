import re
import random

class FallbackContentGenerator:
    def __init__(self):
        pass
    
    def generate_content(self, prompt, platform, original_content=""):
        """Generate platform-optimized content as fallback"""
        
        if platform == "twitter":
            return self._generate_twitter_content(original_content, prompt)
        elif platform == "linkedin":
            return self._generate_linkedin_content(original_content, prompt)
        elif platform == "newsletter":
            return self._generate_newsletter_content(original_content, prompt)
        else:
            return self._generate_generic_content(original_content, prompt)
    
    def _generate_twitter_content(self, content, instructions):
        """Generate Twitter-optimized content"""
        sentences = re.split(r'[.!?]+', content)
        main_tweet = sentences[0] if sentences else content[:200]
        
        tweet = main_tweet.strip()[:250]
        if not tweet.endswith(('.', '!', '?')):
            tweet += '.'
        
        hashtags = self._extract_hashtags(content)
        if hashtags and len(tweet + " " + hashtags) <= 280:
            tweet += f" {hashtags}"
        
        return tweet
    
    def _generate_linkedin_content(self, content, instructions):
        """Generate LinkedIn-optimized content"""
        paragraphs = content.split('. ')
        intro = paragraphs[0] if paragraphs else content[:500]
        
        linkedin_post = f"{intro}.\n\n"
        
        if len(paragraphs) > 1:
            key_points = paragraphs[1:min(4, len(paragraphs))]
            for point in key_points:
                linkedin_post += f"• {point.strip()}.\n"
        
        linkedin_post += f"\n#ContentStrategy #DigitalMarketing"
        return linkedin_post[:3000]
    
    def _generate_newsletter_content(self, content, instructions):
        """Generate newsletter content"""
        newsletter = f"""
Hello,

{content}

Best regards,
Content Team
"""
        return newsletter.strip()
    
    def _generate_generic_content(self, content, instructions):
        return content[:1000]
    
    def _extract_hashtags(self, content):
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        common_words = {'this', 'that', 'with', 'from', 'your', 'have', 'more', 'what'}
        unique_words = [word for word in words if word not in common_words][:3]
        return ' '.join([f'#{word.title()}' for word in unique_words])