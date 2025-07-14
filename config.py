"""
Configuration settings for the Reddit Persona Generator
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for Reddit Persona Generator"""
    
    # Reddit API Configuration
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditPersonaGenerator/1.0')
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Scraping Configuration
    MAX_POSTS = int(os.getenv('MAX_POSTS', 50))
    MAX_COMMENTS = int(os.getenv('MAX_COMMENTS', 100))
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 1))
    
    # Output Configuration
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'user_personas')
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_configs = [
            ('REDDIT_CLIENT_ID', cls.REDDIT_CLIENT_ID),
            ('REDDIT_CLIENT_SECRET', cls.REDDIT_CLIENT_SECRET),
            ('GEMINI_API_KEY', cls.GEMINI_API_KEY)
        ]
        
        missing_configs = []
        for config_name, config_value in required_configs:
            if not config_value:
                missing_configs.append(config_name)
        
        if missing_configs:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_configs)}. "
                f"Please set these environment variables or create a .env file."
            )
        
        return True 