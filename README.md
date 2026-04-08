#  Sales Intelligence Automator

##  Overview
Sales teams spend significant time researching leads before outreach. This project automates that process by collecting company data from the web and generating structured, AI-powered sales insights.

The system accepts raw leads (URLs or company names), gathers relevant information, and produces a structured sales brief including company overview, services, target audience, B2B qualification, and suggested sales questions.

---

#  Project Structure

```
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

Install dependencies:

```bash
pip install -r requirements.txt
```

#  Environment Setup

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

#  How to Run the Project

1. Start the backend server
```bash
uvicorn app.main:app --reload
```

2. Open the application

Go to: http://127.0.0.1:8000

The web interface will load automatically.

#  How to Use the Web Interface

Enter leads (one per line):
- Website URLs OR
- Company names (even incomplete)

Click "Analyze Leads"
The system will:
1. Resolve company names to websites
2. Scrape relevant content (homepage + internal pages)
3. Analyze using LLM
4. Display structured results

If scraping fails:
- The system uses AI fallback
- Results are marked as "(AI Generated)"

#  Design Notes

## System Architecture

The system is designed as a modular pipeline with clearly separated stages: lead ingestion, website resolution, web scraping, content cleaning, and LLM-based analysis. Each lead is processed independently, enabling scalability and future integration with asynchronous job queues or external systems like CRMs.

The scraper first attempts to resolve company names into actual websites using DuckDuckGo search. It then extracts content from the homepage and a limited number of internal links to balance performance and data richness. The cleaned content is passed to the LLM for structured analysis.

## Technology Choices

FastAPI was chosen for its simplicity, speed, and built-in support for async processing. Requests and BeautifulSoup provide a lightweight and reliable scraping solution suitable for this prototype. OpenAI's LLM was used for generating structured business insights due to its strong natural language understanding capabilities.

DuckDuckGo was used instead of Google to avoid scraping restrictions and improve reliability in resolving company names to websites.

## Handling Edge Cases

Real-world web scraping is inherently unreliable. This system includes multiple safeguards:
- Retry logic for failed HTTP requests
- Query cleaning and fallback strategies for noisy lead inputs
- Handling of redirect URLs from search engines
- Content size limiting to prevent LLM overload
- Graceful fallback to AI-based inference when scraping fails

If a website cannot be accessed or parsed, the system still generates useful insights using the lead input and clearly labels the result as AI-generated.

## LLM Reliability & Validation

To ensure consistent and structured outputs, prompt engineering is used to enforce strict JSON responses. A validation layer checks for required fields and correct structure before returning results.

Low temperature settings are used to reduce randomness and improve determinism. In case of invalid or failed responses, fallback logic ensures the system remains robust.

## Future Improvements

Given more time, the following enhancements would be implemented:
- Headless browser scraping (e.g., Playwright) for JavaScript-heavy websites
- Multi-source enrichment (search APIs, business directories)
- Smarter page selection (prioritizing "About" and "Services" pages)
- Vector database + RAG for improved context retrieval
- Persistent storage (PostgreSQL) for lead history
- Background task queue (Celery) for large-scale processing
