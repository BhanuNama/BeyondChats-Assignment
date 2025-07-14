#!/usr/bin/env python3
"""
Setup script for Reddit Persona Generator
Helps users validate their configuration and set up the environment
"""

import os
import sys
from pathlib import Path

def create_env_example():
    """Create .env.example file for users to copy"""
    env_example_content = """# Copy this file to .env and fill in your actual API keys
# Do not commit .env to version control!

# Reddit API Configuration
# Get these from: https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=RedditPersonaGenerator/1.0

# Google Gemini Configuration
# Get this from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Scraping Configuration
MAX_POSTS=50
MAX_COMMENTS=100
REQUEST_DELAY=1

# Output Configuration
OUTPUT_DIR=user_personas
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example_content)
    
    print("Created .env.example file")


def check_dependencies():
    """Check if all required dependencies are installed"""
    # Package name -> import name mapping
    package_mappings = {
        'praw': 'praw',
        'google-generativeai': 'google.generativeai',
        'python-dotenv': 'dotenv',
        'requests': 'requests',
        'tqdm': 'tqdm'
    }
    
    missing_packages = []
    
    for package_name, import_name in package_mappings.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f" Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print(" All required packages are installed")
        return True


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print(" .env file not found")
        print("Copy .env.example to .env and fill in your API keys")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'GEMINI_API_KEY'
    ]
    
    missing_vars = []
    placeholder_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif value.endswith('_here') or 'your_' in value:
            placeholder_vars.append(var)
    
    if missing_vars:
        print(f" Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    if placeholder_vars:
        print(f" Placeholder values found: {', '.join(placeholder_vars)}")
        print("Please replace with your actual API keys")
        return False
    
    print(" Environment variables are configured")
    return True


def test_reddit_connection():
    """Test Reddit API connection"""
    try:
        from config import Config
        from reddit_scraper import RedditScraper
        
        Config.validate_config()
        scraper = RedditScraper()
        print(" Reddit API connection successful")
        return True
        
    except Exception as e:
        print(f" Reddit API connection failed: {e}")
        return False


def test_gemini_connection():
    """Test Google Gemini API connection"""
    try:
        from config import Config
        
        # Check if API key exists and is not placeholder
        if not Config.GEMINI_API_KEY or 'your_' in Config.GEMINI_API_KEY:
            print(" Gemini API key not configured properly")
            return False
        
        # Test Gemini connection
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test request
        response = model.generate_content("Say 'Gemini working!'")
        
        print(" Gemini API connection successful")
        print(f"   Response: {response.text[:50]}...")
        return True
        
    except Exception as e:
        print(f" Gemini API connection failed: {e}")
        print("This might be due to:")
        print("- Invalid or missing Gemini API key") 
        print("- Insufficient API quota")
        print("- Network connectivity issues")
        return False


def main():
    """Main setup function"""
    print(" Reddit Persona Generator Setup")
    print("=" * 50)
    
    # Create .env.example
    create_env_example()
    
    # Check dependencies
    print("\n Checking dependencies...")
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\nPlease install dependencies first:")
        print("pip install -r requirements.txt")
        return 1
    
    # Check environment file
    print("\n Checking environment configuration...")
    env_ok = check_env_file()
    
    if not env_ok:
        print("\nPlease configure your .env file with API keys:")
        print("1. Copy .env.example to .env")
        print("2. Add your Reddit API credentials")
        print("3. Add your Gemini API key from https://aistudio.google.com/app/apikey")
        print("4. Run this setup script again")
        return 1
    
    # Test API connections
    print("\n🔌 Testing API connections...")
    
    reddit_ok = test_reddit_connection()
    gemini_ok = test_gemini_connection()
    
    if reddit_ok and gemini_ok:
        print("\n Setup complete! You can now run the persona generator:")
        print("python reddit_persona_generator.py https://www.reddit.com/user/username/")
        return 0
    else:
        print("\n Setup incomplete. Please fix the API connection issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 