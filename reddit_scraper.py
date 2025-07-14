"""
Reddit User Data Scraper using PRAW
"""
import praw
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
from tqdm import tqdm
from config import Config


@dataclass
class RedditPost:
    """Data structure for Reddit posts"""
    id: str
    title: str
    selftext: str
    subreddit: str
    score: int
    num_comments: int
    created_utc: float
    url: str
    permalink: str


@dataclass
class RedditComment:
    """Data structure for Reddit comments"""
    id: str
    body: str
    subreddit: str
    score: int
    created_utc: float
    permalink: str
    parent_id: str


class RedditScraper:
    """Reddit scraper class using PRAW"""
    
    def __init__(self):
        """Initialize Reddit scraper with API credentials"""
        self.reddit = None
        self._initialize_reddit_client()
    
    def _initialize_reddit_client(self):
        """Initialize the Reddit client with proper authentication"""
        try:
            self.reddit = praw.Reddit(
                client_id=Config.REDDIT_CLIENT_ID,
                client_secret=Config.REDDIT_CLIENT_SECRET,
                user_agent=Config.REDDIT_USER_AGENT
            )
            # Test the connection
            self.reddit.user.me()
        except Exception as e:
            print(f"Failed to initialize Reddit client: {e}")
            print("Please check your Reddit API credentials in the .env file")
            raise
    
    def extract_username_from_url(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        # Handle various URL formats
        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
            r'www\.reddit\.com/user/([^/]+)',
            r'www\.reddit\.com/u/([^/]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, profile_url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract username from URL: {profile_url}")
    
    def get_user_posts(self, username: str, max_posts: int = None) -> List[RedditPost]:
        """Scrape user's posts"""
        if max_posts is None:
            max_posts = Config.MAX_POSTS
        
        posts = []
        try:
            user = self.reddit.redditor(username)
            
            print(f"Scraping posts for user: {username}")
            post_submissions = list(user.submissions.new(limit=max_posts))
            
            for submission in tqdm(post_submissions, desc="Extracting posts"):
                try:
                    post = RedditPost(
                        id=submission.id,
                        title=submission.title or "",
                        selftext=submission.selftext or "",
                        subreddit=str(submission.subreddit),
                        score=submission.score,
                        num_comments=submission.num_comments,
                        created_utc=submission.created_utc,
                        url=submission.url,
                        permalink=f"https://reddit.com{submission.permalink}"
                    )
                    posts.append(post)
                    
                    # Rate limiting
                    time.sleep(Config.REQUEST_DELAY)
                    
                except Exception as e:
                    print(f"Error processing post {submission.id}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching posts for user {username}: {e}")
            raise
        
        return posts
    
    def get_user_comments(self, username: str, max_comments: int = None) -> List[RedditComment]:
        """Scrape user's comments"""
        if max_comments is None:
            max_comments = Config.MAX_COMMENTS
        
        comments = []
        try:
            user = self.reddit.redditor(username)
            
            print(f"Scraping comments for user: {username}")
            comment_submissions = list(user.comments.new(limit=max_comments))
            
            for comment in tqdm(comment_submissions, desc="Extracting comments"):
                try:
                    # Skip deleted/removed comments
                    if comment.body in ['[deleted]', '[removed]']:
                        continue
                    
                    reddit_comment = RedditComment(
                        id=comment.id,
                        body=comment.body or "",
                        subreddit=str(comment.subreddit),
                        score=comment.score,
                        created_utc=comment.created_utc,
                        permalink=f"https://reddit.com{comment.permalink}",
                        parent_id=comment.parent_id
                    )
                    comments.append(reddit_comment)
                    
                    # Rate limiting
                    time.sleep(Config.REQUEST_DELAY)
                    
                except Exception as e:
                    print(f"Error processing comment {comment.id}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching comments for user {username}: {e}")
            raise
        
        return comments
    
    def get_user_data(self, profile_url: str) -> Tuple[List[RedditPost], List[RedditComment]]:
        """Get all user data (posts and comments) from profile URL"""
        username = self.extract_username_from_url(profile_url)
        
        print(f"Starting data collection for Reddit user: {username}")
        print(f"Profile URL: {profile_url}")
        
        # Check if user exists
        try:
            user = self.reddit.redditor(username)
            # This will raise an exception if user doesn't exist
            user.id
        except Exception:
            raise ValueError(f"Reddit user '{username}' does not exist or is suspended")
        
        posts = self.get_user_posts(username)
        comments = self.get_user_comments(username)
        
        print(f"Successfully scraped {len(posts)} posts and {len(comments)} comments")
        
        return posts, comments
    
    def get_user_stats(self, username: str) -> Dict:
        """Get basic user statistics"""
        try:
            user = self.reddit.redditor(username)
            
            stats = {
                'username': username,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'total_karma': user.comment_karma + user.link_karma,
                'account_age_days': (datetime.now().timestamp() - user.created_utc) / 86400,
                'has_verified_email': getattr(user, 'has_verified_email', None),
                'is_employee': getattr(user, 'is_employee', False),
                'is_mod': getattr(user, 'is_mod', False),
                'is_gold': getattr(user, 'is_gold', False)
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting user stats for {username}: {e}")
            return {'username': username, 'error': str(e)} 