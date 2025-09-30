import streamlit as st
import json
from perplexity_client import PerplexityClient
from content_processor import ContentProcessor
from fallback_generator import FallbackContentGenerator

# Initialize clients
perplexity_client = PerplexityClient()
content_processor = ContentProcessor()
fallback_generator = FallbackContentGenerator()

# Streamlit app configuration
st.set_page_config(
    page_title="Content Distribution Pipeline",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .platform-section {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    .sentiment-positive { color: #4CAF50; }
    .sentiment-negative { color: #F44336; }
    .sentiment-neutral { color: #FF9800; }
</style>
""", unsafe_allow_html=True)

def safe_generate_content(original_content, additional_prompt, platform):
    """Safely generate content with fallback"""
    try:
        # Try Perplexity API first
        content = perplexity_client.generate_content(
            additional_prompt, platform.lower(), original_content
        )
        
        # Check if API returned an error message
        if content.startswith(('Error', 'HTTP Error', 'Request Error')):
            st.warning(f"API Issue: Using fallback generator for {platform}")
            return fallback_generator.generate_content(
                additional_prompt, platform.lower(), original_content
            )
        
        return content
        
    except Exception as e:
        st.warning(f"Using fallback content generator for {platform}")
        return fallback_generator.generate_content(
            additional_prompt, platform.lower(), original_content
        )

def main():
    st.markdown('<div class="main-header">🚀 Content Distribution Pipeline</div>', unsafe_allow_html=True)
    
    # Sidebar for input
    with st.sidebar:
        st.header("Content Input")
        original_content = st.text_area(
            "Enter your content:",
            height=200,
            placeholder="Paste your article, blog post, or content idea here..."
        )
        
        additional_prompt = st.text_area(
            "Additional instructions:",
            height=100,
            placeholder="Any specific tone, style, or requirements..."
        )
        
        platforms = st.multiselect(
            "Select platforms to generate for:",
            ["Twitter", "LinkedIn", "Newsletter"],
            default=["Twitter", "LinkedIn", "Newsletter"]
        )
        
        generate_button = st.button("Generate Content", type="primary", use_container_width=True)
    
    # Main content area
    if generate_button and original_content:
        if not platforms:
            st.warning("Please select at least one platform.")
            return
        
        # Analyze original content
        with st.spinner("Analyzing content and generating platform-specific versions..."):
            sentiment = content_processor.analyze_sentiment(original_content)
            stats = content_processor.get_content_stats(original_content)
            
            # Display analysis results
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Word Count", stats["word_count"])
            with col2:
                st.metric("Reading Time", f"{stats['reading_time']} min")
            with col3:
                sentiment_color = f"sentiment-{sentiment['sentiment']}"
                st.markdown(f'<div class="{sentiment_color}">Sentiment: {sentiment["sentiment"].upper()}</div>', unsafe_allow_html=True)
            with col4:
                st.metric("Polarity", f"{sentiment['polarity']:.3f}")
        
        # Generate content for each platform
        for platform in platforms:
            st.markdown(f'<div class="platform-section"><h3>📱 {platform} Content</h3></div>', unsafe_allow_html=True)
            
            with st.spinner(f"Generating {platform} content..."):
                # Use the safe generation function
                generated_content = safe_generate_content(original_content, additional_prompt, platform)
                
                # Platform-specific formatting
                if platform.lower() == "twitter":
                    tweets = content_processor.format_twitter_thread(generated_content)
                    for i, tweet in enumerate(tweets, 1):
                        st.text_area(f"Tweet {i}/{len(tweets)}", tweet, height=100, key=f"tweet_{i}_{platform}")
                        st.caption(f"Character count: {len(tweet)}")
                        
                elif platform.lower() == "linkedin":
                    linkedin_content = content_processor.format_linkedin_post(generated_content)
                    st.text_area("LinkedIn Post", linkedin_content, height=200, key=f"linkedin_{platform}")
                    st.caption(f"Character count: {len(linkedin_content)}")
                    
                elif platform.lower() == "newsletter":
                    subject_line = f"Newsletter: {original_content[:50]}..." if original_content else "Newsletter Update"
                    newsletter_content = content_processor.format_newsletter(generated_content, subject_line)
                    st.text_area("Newsletter Content", newsletter_content, height=300, key=f"newsletter_{platform}")
                    st.caption(f"Character count: {len(newsletter_content)}")
                
                # Sentiment analysis for generated content
                gen_sentiment = content_processor.analyze_sentiment(generated_content)
                st.info(f"Generated content sentiment: {gen_sentiment['sentiment'].upper()} "
                       f"(Polarity: {gen_sentiment['polarity']:.3f}, "
                       f"Subjectivity: {gen_sentiment['subjectivity']:.3f})")
    
    elif generate_button and not original_content:
        st.error("Please enter some content to generate platform-specific versions.")
    
    else:
        # Welcome message and instructions
        st.info("""
        **Welcome to the Content Distribution Pipeline!**
        
        This AI-powered tool helps you adapt your content for different platforms automatically.
        
        **How to use:**
        1. Paste your content in the sidebar
        2. Add any specific instructions
        3. Select the platforms you want to target
        4. Click "Generate Content"
        
        **Features:**
        - ✅ Automatic platform-specific formatting
        - ✅ Sentiment analysis
        - ✅ Twitter thread generation
        - ✅ LinkedIn professional formatting
        - ✅ Newsletter template creation
        - ✅ Content statistics and insights
        - ✅ Fallback content generation (if API fails)
        """)

if __name__ == "__main__":

    main()
