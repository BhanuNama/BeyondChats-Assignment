#!/usr/bin/env python3
"""
Reddit User Persona Generator
Main script to scrape Reddit user data and generate detailed personas

Usage:
    python reddit_persona_generator.py https://www.reddit.com/user/username/
    python reddit_persona_generator.py --help
"""

import sys
import argparse
import traceback
from datetime import datetime
from pathlib import Path

from config import Config
from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator


def setup_output_directory():
    """Create output directory for persona files"""
    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    return output_dir


def save_persona_to_file(persona_text: str, username: str, output_dir: Path) -> str:
    """Save persona to a text file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}_persona_{timestamp}.txt"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(persona_text)
    
    return str(filepath)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate user personas from Reddit profiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python reddit_persona_generator.py https://www.reddit.com/user/kojied/
    python reddit_persona_generator.py https://www.reddit.com/user/Hungry-Move-6603/
    python reddit_persona_generator.py --url https://www.reddit.com/user/username/ --max-posts 30 --max-comments 50

Required Environment Variables:
    REDDIT_CLIENT_ID     - Reddit API client ID
    REDDIT_CLIENT_SECRET - Reddit API client secret
    GEMINI_API_KEY       - Gemini API key

Optional Environment Variables:
    REDDIT_USER_AGENT    - Reddit API user agent (default: RedditPersonaGenerator/1.0)
    MAX_POSTS           - Maximum posts to analyze (default: 50)
    MAX_COMMENTS        - Maximum comments to analyze (default: 100)
    OUTPUT_DIR          - Output directory for persona files (default: user_personas)
    REQUEST_DELAY       - Delay between API requests in seconds (default: 1)
        """
    )
    
    parser.add_argument(
        'profile_url',
        nargs='?',
        help='Reddit user profile URL (e.g., https://www.reddit.com/user/username/)'
    )
    
    parser.add_argument(
        '--url',
        help='Alternative way to specify the Reddit profile URL'
    )
    
    parser.add_argument(
        '--max-posts',
        type=int,
        default=Config.MAX_POSTS,
        help=f'Maximum number of posts to analyze (default: {Config.MAX_POSTS})'
    )
    
    parser.add_argument(
        '--max-comments',
        type=int,
        default=Config.MAX_COMMENTS,
        help=f'Maximum number of comments to analyze (default: {Config.MAX_COMMENTS})'
    )
    
    parser.add_argument(
        '--output-dir',
        default=Config.OUTPUT_DIR,
        help=f'Output directory for persona files (default: {Config.OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def validate_profile_url(url: str) -> bool:
    """Validate that the provided URL is a valid Reddit profile URL"""
    if not url:
        return False
    
    valid_patterns = [
        'reddit.com/user/',
        'reddit.com/u/',
        'www.reddit.com/user/',
        'www.reddit.com/u/'
    ]
    
    return any(pattern in url.lower() for pattern in valid_patterns)


def main():
    """Main function"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Get profile URL
        profile_url = args.profile_url or args.url
        
        if not profile_url:
            print("Error: Please provide a Reddit profile URL")
            print("Usage: python reddit_persona_generator.py https://www.reddit.com/user/username/")
            print("Use --help for more information")
            sys.exit(1)
        
        # Validate URL
        if not validate_profile_url(profile_url):
            print(f"Error: Invalid Reddit profile URL: {profile_url}")
            print("Expected format: https://www.reddit.com/user/username/")
            sys.exit(1)
        
        # Validate configuration
        try:
            Config.validate_config()
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("\nTo set up the required environment variables:")
            print("1. Create a .env file in the project directory")
            print("2. Add the following variables:")
            print("   REDDIT_CLIENT_ID=your_reddit_client_id")
            print("   REDDIT_CLIENT_SECRET=your_reddit_client_secret")
            print("   GEMINI_API_KEY=your_gemini_api_key")
            print("\nSee README.md for detailed setup instructions.")
            sys.exit(1)
        
        # Override config with command line arguments
        Config.MAX_POSTS = args.max_posts
        Config.MAX_COMMENTS = args.max_comments
        Config.OUTPUT_DIR = args.output_dir
        
        if args.verbose:
            print(f"Configuration:")
            print(f"  Max Posts: {Config.MAX_POSTS}")
            print(f"  Max Comments: {Config.MAX_COMMENTS}")
            print(f"  Output Directory: {Config.OUTPUT_DIR}")
            print(f"  Request Delay: {Config.REQUEST_DELAY}s")
            print()
        
        # Setup output directory
        output_dir = setup_output_directory()
        
        # Initialize components
        print("Initializing Reddit scraper...")
        scraper = RedditScraper()
        
        print("Initializing persona generator...")
        generator = PersonaGenerator()
        
        # Extract username from URL
        username = scraper.extract_username_from_url(profile_url)
        
        print(f"Starting analysis for Reddit user: {username}")
        print(f"Profile URL: {profile_url}")
        print("=" * 60)
        
        # Scrape user data
        print("\n1. Scraping Reddit data...")
        posts, comments = scraper.get_user_data(profile_url)
        
        if not posts and not comments:
            print("Warning: No posts or comments found for this user.")
            print("This could mean:")
            print("- The user has no public content")
            print("- The user account is suspended or deleted")
            print("- The user has privacy settings enabled")
            sys.exit(1)
        
        # Get user statistics
        user_stats = scraper.get_user_stats(username)
        
        print(f"Data collection complete:")
        print(f"  Posts found: {len(posts)}")
        print(f"  Comments found: {len(comments)}")
        print(f"  Account karma: {user_stats.get('total_karma', 'N/A')}")
        
        # Generate persona
        print("\n2. Generating user persona...")
        persona = generator.generate_persona(username, posts, comments, user_stats)
        
        # Format as text
        print("\n3. Formatting persona output...")
        persona_text = generator.format_persona_as_text(persona)
        
        # Save to file
        print("\n4. Saving persona to file...")
        output_file = save_persona_to_file(persona_text, username, output_dir)
        
        print("=" * 60)
        print("✅ PERSONA GENERATION COMPLETE!")
        print(f"   Username: {username}")
        print(f"   Output file: {output_file}")
        print(f"   Posts analyzed: {len(posts)}")
        print(f"   Comments analyzed: {len(comments)}")
        print("=" * 60)
        
        # Show brief summary
        if persona.summary:
            print(f"\nBrief Summary:")
            print(f"{persona.summary}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
        if args.verbose if 'args' in locals() else False:
            print("\nFull traceback:")
            traceback.print_exc()
        else:
            print("Use --verbose for detailed error information.")
        
        return 1


if __name__ == "__main__":
    sys.exit(main()) 