#  Sales Intelligence Automator

##  Overview
Sales teams spend significant time researching leads before outreach. This project automates that process by collecting company data from the web and generating structured, AI-powered sales insights.

The system accepts raw leads (URLs or company names), gathers relevant information, and produces a structured sales brief including:
- Company Overview
- Core Product/Service
- Target Customer
- B2B Qualification
- Suggested Sales Questions

---

#  Project Structure

```text
sales-intelligence-automator/
│
├── app/
│ ├── main.py # FastAPI backend
│ ├── scraper.py # Web scraping + lead resolution
│ ├── llm.py # LLM integration
│ ├── validator.py # Output validation
│
├── frontend/
│ ├── index.html # Web UI
│ └── style.css # Styling
│
├── .devcontainer/
│ └── devcontainer.json # Codespaces setup
│
├── requirements.txt
└── README.md
```

---

#  Dependencies

- Python 3.9+
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- OpenAI
- Python-dotenv

---

#  Run Using GitHub Codespaces (Recommended)

This project is fully configured to run in GitHub Codespaces with minimal setup.

## Steps:

1. Open the repository on GitHub  
2. Click **Code → Codespaces → Create Codespace**  
3. Wait for environment setup (dependencies auto-install)

---

##  Set API Key

Run in terminal:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Or add it in:

GitHub → Settings → Secrets → Codespaces

###  Run the Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

###  Open the Application

- Go to Ports tab
- Open Port 8000
- The web UI will load automatically

###  Run Locally (Optional)

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

##  How to Use the Web Interface

Enter leads (one per line):
- Website URLs OR
- Company names (even incomplete)

Click "Analyze Leads"
The system will:
- Resolve company names to websites
- Scrape homepage + internal pages
- Analyze using LLM
- Display structured results

If scraping fails:
- AI fallback is used
- Result is labeled "(AI Generated)"

# System Architecture

The system is designed as a modular pipeline consisting of lead ingestion, website resolution, web scraping, content cleaning, and LLM-based analysis. Each lead is processed independently, enabling scalability and future integration with CRMs or background processing systems.

The scraper resolves company names into real websites using DuckDuckGo and extracts content from the homepage and selected internal pages to ensure meaningful context.

# Technology Choices

FastAPI was chosen for its asynchronous capabilities and simplicity in building APIs. Requests and BeautifulSoup provide a lightweight yet effective scraping solution.

OpenAI LLM is used for generating structured business insights due to its strong natural language understanding. DuckDuckGo was selected over Google to reduce scraping restrictions.

# Handling Edge Cases

Real-world web scraping is unreliable, so multiple safeguards were implemented:

- Retry logic for failed requests
- Query cleaning for noisy lead inputs
- Handling redirect URLs from search engines
- Limiting number of pages scraped for performance
- Graceful fallback to AI when scraping fails

This ensures the system continues to provide value even when web data is unavailable.

# LLM Reliability

Strict prompt design ensures structured JSON output. A validation layer checks for required fields and format correctness.

Low temperature settings reduce randomness and improve consistency. Fallback handling ensures robustness even when the model output is imperfect.

# Future Improvements

With more time, the system can be enhanced with:

- Headless browser scraping (Playwright) for JavaScript-heavy sites
- Smarter page selection (About, Services prioritization)
- Multi-source enrichment APIs
- Vector database + RAG pipeline
- PostgreSQL for persistent storage
- Background job queue (Celery)

