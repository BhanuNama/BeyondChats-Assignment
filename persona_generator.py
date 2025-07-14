"""
User Persona Generator using Google Gemini 1.5 Pro
"""
import json
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
import google.generativeai as genai
from config import Config
from reddit_scraper import RedditPost, RedditComment


@dataclass
class PersonaCharacteristic:
    """Data structure for persona characteristics"""
    category: str
    trait: str
    confidence: str
    description: str
    evidence: List[str]
    citations: List[str]


@dataclass
class UserPersona:
    """Complete user persona data structure"""
    username: str
    generated_date: str
    account_stats: Dict
    demographics: List[PersonaCharacteristic]
    interests: List[PersonaCharacteristic]
    personality: List[PersonaCharacteristic]
    behavior_patterns: List[PersonaCharacteristic]
    communication_style: List[PersonaCharacteristic]
    values_beliefs: List[PersonaCharacteristic]
    summary: str
    data_sources: Dict


class PersonaGenerator:
    """Gemini-powered persona generator"""
    
    def __init__(self):
        """Initialize the persona generator with Gemini"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.max_content_length = 15000  # Gemini can handle more content
    
    def _prepare_content_for_analysis(self, posts: List[RedditPost], comments: List[RedditComment]) -> str:
        """Prepare content for Gemini analysis"""
        content_parts = []
        
        # Add posts
        content_parts.append("=== REDDIT POSTS ===\n")
        for i, post in enumerate(posts[:30], 1):  # More posts since Gemini handles more content
            content_parts.append(f"POST {i}:\n")
            content_parts.append(f"Subreddit: r/{post.subreddit}\n")
            content_parts.append(f"Title: {post.title}\n")
            if post.selftext:
                content_parts.append(f"Content: {post.selftext[:800]}\n")
            content_parts.append(f"Score: {post.score}, Comments: {post.num_comments}\n")
            content_parts.append(f"URL: {post.permalink}\n\n")
        
        # Add comments
        content_parts.append("=== REDDIT COMMENTS ===\n")
        for i, comment in enumerate(comments[:50], 1):  # More comments
            content_parts.append(f"COMMENT {i}:\n")
            content_parts.append(f"Subreddit: r/{comment.subreddit}\n")
            content_parts.append(f"Content: {comment.body[:500]}\n")
            content_parts.append(f"Score: {comment.score}\n")
            content_parts.append(f"URL: {comment.permalink}\n\n")
        
        full_content = "".join(content_parts)
        
        # Truncate if too long
        if len(full_content) > self.max_content_length:
            full_content = full_content[:self.max_content_length] + "\n[CONTENT TRUNCATED]"
        
        return full_content
    
    def _create_analysis_prompt(self, username: str, content: str, user_stats: Dict) -> str:
        """Create the prompt for Gemini analysis"""
        return f"""
Analyze the following Reddit user data and create a comprehensive user persona for "{username}".

ACCOUNT STATISTICS:
{json.dumps(user_stats, indent=2)}

USER CONTENT:
{content}

TASK: Create a detailed user persona with the following categories:

1. DEMOGRAPHICS (age range, location hints, occupation clues, education level)
2. INTERESTS (hobbies, topics of interest, favorite subreddits)  
3. PERSONALITY (traits, emotional patterns, social preferences)
4. BEHAVIOR PATTERNS (posting frequency, engagement style, content preferences)
5. COMMUNICATION STYLE (tone, language use, interaction patterns)
6. VALUES & BELIEFS (political leanings, moral stances, worldviews)

For each characteristic, provide:
- Specific trait name
- Confidence level (High/Medium/Low)
- Brief description/explanation
- Direct evidence quotes from their posts/comments
- Citations with post/comment URLs

IMPORTANT: Format your response as valid JSON with this exact structure:

{{
    "demographics": [
        {{
            "trait": "Age Range",
            "confidence": "Medium",
            "description": "Explanation based on evidence",
            "evidence": ["exact quote from post/comment"],
            "citations": ["URL link"]
        }}
    ],
    "interests": [...],
    "personality": [...],
    "behavior_patterns": [...],
    "communication_style": [...],
    "values_beliefs": [...],
    "summary": "2-3 sentence overall summary of the user's persona"
}}

Be thorough but only include characteristics you can support with concrete evidence from the provided content.
"""
    
    def generate_persona(self, username: str, posts: List[RedditPost], comments: List[RedditComment], user_stats: Dict) -> UserPersona:
        """Generate a complete user persona from Reddit data"""
        print(f"Generating persona for user: {username}")
        
        # Prepare content for analysis
        content = self._prepare_content_for_analysis(posts, comments)
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(username, content, user_stats)
        
        try:
            # Get Gemini analysis
            print("Analyzing data with Google Gemini 1.5 Flash...")
            response = self.model.generate_content(prompt)
            
            # Parse the JSON response
            response_text = response.text
            
            # Extract JSON from the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in Gemini response")
            
            json_str = response_text[json_start:json_end]
            parsed_data = json.loads(json_str)
            
            # Convert to structured persona
            persona = UserPersona(
                username=username,
                generated_date=datetime.now().isoformat(),
                account_stats=user_stats,
                demographics=self._convert_to_characteristics("Demographics", parsed_data.get('demographics', [])),
                interests=self._convert_to_characteristics("Interests", parsed_data.get('interests', [])),
                personality=self._convert_to_characteristics("Personality", parsed_data.get('personality', [])),
                behavior_patterns=self._convert_to_characteristics("Behavior Patterns", parsed_data.get('behavior_patterns', [])),
                communication_style=self._convert_to_characteristics("Communication Style", parsed_data.get('communication_style', [])),
                values_beliefs=self._convert_to_characteristics("Values & Beliefs", parsed_data.get('values_beliefs', [])),
                summary=parsed_data.get('summary', ''),
                data_sources={
                    'posts_analyzed': len(posts),
                    'comments_analyzed': len(comments)
                }
            )
            
            print("Persona generation completed successfully!")
            return persona
            
        except Exception as e:
            print(f"Error generating persona: {e}")
            raise
    
    def _convert_to_characteristics(self, category: str, traits_data: List[Dict]) -> List[PersonaCharacteristic]:
        """Convert response data to PersonaCharacteristic objects"""
        characteristics = []
        
        for trait_data in traits_data:
            try:
                characteristic = PersonaCharacteristic(
                    category=category,
                    trait=trait_data.get('trait', ''),
                    confidence=trait_data.get('confidence', 'Unknown'),
                    description=trait_data.get('description', ''),
                    evidence=trait_data.get('evidence', []),
                    citations=trait_data.get('citations', [])
                )
                characteristics.append(characteristic)
            except Exception as e:
                print(f"Error converting trait data: {e}")
                continue
        
        return characteristics
    
    def format_persona_as_text(self, persona: UserPersona) -> str:
        """Format the persona as a readable text file"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append(f"REDDIT USER PERSONA: {persona.username}")
        output.append("=" * 80)
        output.append(f"Generated on: {persona.generated_date}")
        output.append(f"Powered by: Google Gemini 1.5 Flash")
        output.append(f"Data analyzed: {persona.data_sources['posts_analyzed']} posts, {persona.data_sources['comments_analyzed']} comments")
        output.append("")
        
        # Account Statistics
        output.append("ACCOUNT STATISTICS")
        output.append("-" * 40)
        stats = persona.account_stats
        if 'account_age_days' in stats:
            output.append(f"Account Age: {stats.get('account_age_days', 0):.0f} days")
        output.append(f"Comment Karma: {stats.get('comment_karma', 'N/A')}")
        output.append(f"Link Karma: {stats.get('link_karma', 'N/A')}")
        output.append(f"Total Karma: {stats.get('total_karma', 'N/A')}")
        output.append("")
        
        # Summary
        output.append("PERSONA SUMMARY")
        output.append("-" * 40)
        output.append(persona.summary)
        output.append("")
        
        # Categories
        categories = [
            ("DEMOGRAPHICS", persona.demographics),
            ("INTERESTS", persona.interests),
            ("PERSONALITY TRAITS", persona.personality),
            ("BEHAVIOR PATTERNS", persona.behavior_patterns),
            ("COMMUNICATION STYLE", persona.communication_style),
            ("VALUES & BELIEFS", persona.values_beliefs)
        ]
        
        for category_name, characteristics in categories:
            if characteristics:
                output.append(category_name)
                output.append("-" * 40)
                
                for char in characteristics:
                    output.append(f"• {char.trait}")
                    output.append(f"  Confidence: {char.confidence}")
                    output.append(f"  Description: {char.description}")
                    
                    if char.evidence:
                        output.append("  Evidence:")
                        for evidence in char.evidence:
                            output.append(f"    - \"{evidence[:150]}...\"")
                    
                    if char.citations:
                        output.append("  Citations:")
                        for citation in char.citations:
                            output.append(f"    - {citation}")
                    
                    output.append("")
                
                output.append("")
        
        return "\n".join(output) 