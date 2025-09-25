from textblob import TextBlob
import re
from config import PLATFORM_CONFIG

class ContentProcessor:
    def __init__(self):
        self.platform_config = PLATFORM_CONFIG
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the text"""
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        }
    
    def format_twitter_thread(self, content):
        """Convert long content into Twitter thread format"""
        sentences = re.split(r'[.!?]+', content)
        tweets = []
        current_tweet = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            potential_tweet = f"{current_tweet} {sentence}.".strip() if current_tweet else f"{sentence}."
            
            if len(potential_tweet) <= 250:  # Leave space for (1/5) etc.
                current_tweet = potential_tweet
            else:
                if current_tweet:
                    tweets.append(current_tweet)
                current_tweet = f"{sentence}."
        
        if current_tweet:
            tweets.append(current_tweet)
        
        # Add thread indicators
        if len(tweets) > 1:
            formatted_tweets = []
            for i, tweet in enumerate(tweets, 1):
                indicator = f"({i}/{len(tweets)})"
                formatted_tweets.append(f"{tweet} {indicator}")
            return formatted_tweets
        else:
            return tweets if tweets else [content]
    
    def format_linkedin_post(self, content):
        """Format content for LinkedIn"""
        # Ensure professional structure
        paragraphs = content.split('\n\n')
        formatted_content = "\n\n".join([p.strip() for p in paragraphs if p.strip()])
        
        # Add relevant hashtags based on content
        hashtags = self._generate_hashtags(content)
        if hashtags:
            formatted_content += f"\n\n{hashtags}"
        
        return formatted_content
    
    def format_newsletter(self, content, subject_line):
        """Format content for newsletter"""
        newsletter_template = f"""
SUBJECT: {subject_line}

{content}

---
Best regards,
Content Distribution Team
"""
        return newsletter_template
    
    def _generate_hashtags(self, content, max_hashtags=5):
        """Generate relevant hashtags from content"""
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', content.lower())
        meaningful_words = [word for word in words if word not in common_words and len(word) > 3]
        
        # Get most frequent words
        from collections import Counter
        word_freq = Counter(meaningful_words)
        top_words = [word for word, count in word_freq.most_common(max_hashtags)]
        
        hashtags = ' '.join([f'#{word}' for word in top_words])
        return hashtags
    
    def get_content_stats(self, content):
        """Get statistics about the content"""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "char_count": len(content),
            "reading_time": round(len(words) / 200, 1)  # 200 wpm average
        }