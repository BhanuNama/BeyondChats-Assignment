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

## Use Cases
- **Academic Research**: Analyze online behavior and digital personas for studies.
- **Marketing & UX**: Understand target audiences and user archetypes.
- **Personal Insight**: Discover your own Reddit persona or that of others.
- **Content Moderation**: Profile users for moderation or community management.

---

## How it Works
1. **Input:** You provide a Reddit user profile URL.
2. **Scraping:** The tool collects recent posts and comments using Reddit's API.
3. **Analysis:** Google Gemini analyzes the content to infer persona traits, citing specific posts/comments as evidence.
4. **Output:** A detailed persona file is generated, with each insight linked to supporting Reddit content.

---

## Customization
- **Scraping Limits:** Adjust `MAX_POSTS`, `MAX_COMMENTS`, and `REQUEST_DELAY` in your `.env` file or via command-line arguments.
- **Output Location:** Change `OUTPUT_DIR` in `.env` or use `--output-dir`.
- **Persona Depth:** Edit prompts in `persona_generator.py` to tailor the analysis or add/remove persona categories.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for new features, bug fixes, or improvements.

---

## Prerequisites
- **Reddit API credentials** ([instructions](https://www.reddit.com/prefs/apps))
- **Google Gemini API key** ([get one here](https://aistudio.google.com/app/apikey))
- **Python 3.8+**

---

## Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/BhanuNama/BeyondChats-Assignment
   cd BeyondChats-Assignment
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

## Example Output
```
Persona for Reddit user: kojied

Demographics:
- Likely male, 20s-30s, based on language and interests. [Cited: https://reddit.com/r/examplepost1]

Interests:
- Technology, gaming, and science. [Cited: https://reddit.com/r/examplepost2]

Personality Traits:
- Curious, analytical, and helpful. [Cited: https://reddit.com/r/examplecomment1]

... (see full file for more)
```

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

## Technologies Used
- **Python 3.8+**
- **PRAW** (Python Reddit API Wrapper)
- **Google Gemini API**
- **dotenv** (for environment management)

---

## Troubleshooting
- **API errors:** Check your API keys and quotas
- **No output:** User may have no public content or be suspended
- **Quota errors:** Wait and try again (Gemini Flash has high free limits)

---

## Limitations & Ethics
- **Private/Suspended Users:** Cannot access content from private or suspended accounts.
- **LLM Limitations:** AI-generated personas may contain inaccuracies or hallucinations; always verify critical insights.
- **Ethical Use:** Use responsibly and respect user privacy. Do not use for harassment, surveillance, or any unethical purposes.

---

## License
For educational and research use. Comply with Reddit and Google API terms.

---

## Contact
For questions or support, contact:

**Your Name**  
bhanunama08@gmail.com

