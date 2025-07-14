# Reddit User Persona Generator

A professional tool to analyze Reddit user profiles and generate detailed user personas using Google Gemini 1.5 Flash. The script scrapes a user's posts and comments, then uses advanced AI to create insights about their demographics, interests, personality traits, and behavior patterns.

---

## Features
- **Automated Reddit Data Scraping**: Uses PRAW (official Reddit API) to extract user posts and comments
- **AI-Powered Analysis**: Leverages Google Gemini 1.5 Flash for persona generation
- **Comprehensive Persona**: Demographics, Interests, Personality, Behavior Patterns, Communication Style, Values & Beliefs
- **Evidence & Citations**: Each trait includes supporting quotes and links
- **Easy Setup & Use**: One-command execution, clear config, and output

---

## Prerequisites
- **Reddit API credentials** ([instructions](https://www.reddit.com/prefs/apps))
- **Google Gemini API key** ([get one here](https://aistudio.google.com/app/apikey))
- **Python 3.8+**

---

## Installation & Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd reddit-persona-generator
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in your Reddit and Gemini API keys
4. **Validate setup**
   ```bash
   python setup.py
   ```

---

## Usage
Generate a persona for any Reddit user:
```bash
python reddit_persona_generator.py https://www.reddit.com/user/kojied/
python reddit_persona_generator.py https://www.reddit.com/user/Hungry-Move-6603/
```
- Output will be saved as a `.txt` file in `user_personas/`.

**Advanced options:**
```bash
python reddit_persona_generator.py <profile_url> --max-posts 100 --max-comments 200 --output-dir sample_outputs
```

---

## Sample Output Files
Sample persona files for assignment users are included in the `sample_outputs/` folder:
- `sample_outputs/kojied_persona_*.txt`
- `sample_outputs/Hungry-Move-6603_persona_*.txt`

---

## Configuration
Set these in your `.env` file:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditPersonaGenerator/1.0
GEMINI_API_KEY=your_gemini_api_key
MAX_POSTS=50
MAX_COMMENTS=100
REQUEST_DELAY=1
OUTPUT_DIR=user_personas
```

---

## Project Structure
```
reddit-persona-generator/
├── reddit_persona_generator.py    # Main script
├── reddit_scraper.py             # Reddit data scraper
├── persona_generator.py          # Gemini-powered persona generator
├── config.py                     # Config management
├── setup.py                      # Setup/validation
├── requirements.txt              # Dependencies
├── .gitignore                    # Ignore rules
├── .env.example                  # Example config
├── sample_outputs/               # Sample persona files
└── README.md                     # Documentation
```

---

## Troubleshooting
- **API errors:** Check your API keys and quotas
- **No output:** User may have no public content or be suspended
- **Quota errors:** Wait and try again (Gemini Flash has high free limits)

---

## License
For educational and research use. Comply with Reddit and Google API terms.

---

**Powered by Google Gemini 1.5 Flash** 