# German Startup Investment Screener

An end-to-end agentic pipeline that scrapes German startup data, scores each company
using an LLM, and outputs a ranked investment shortlist, with a visual dashboard.

## What it does

1. Scrapes top German startups from a public directory (failory.com)
2. Sends each company's data to an LLM agent (Groq API / Claude API-ready)
3. Agent scores each company 1-10 based on investment criteria
4. Outputs a ranked CSV with scores, risk level, and rationale
5. Generates a visual HTML dashboard — open in any browser, no server needed

## Project structure

olta_agent/
├── scraper.py            # Web scraping logic (requests + BeautifulSoup)
├── scorer.py             # LLM agent scoring loop (Groq API)
├── report.py             # HTML dashboard generator
├── main.py               # Pipeline orchestrator
├── ranked_companies.csv  # Generated output (rankings)
├── dashboard.html        # Generated output (visual dashboard)
├── .env                  # API keys (never commit this)
├── .gitignore            # Ensures .env is excluded from git
└── README.md

## Setup

pip install requests beautifulsoup4 groq python-dotenv pandas

Add your API key to .env:
GROQ_API_KEY=xxxxxxxxxxxxxxxxx

## Run

python main.py

This will:
- Scrape 10 German startups from failory.com
- Score each one via Groq LLM
- Save ranked_companies.csv
- Generate dashboard.html — open this in your browser to see the results

## Architecture

Scraper → Cleaner → LLM Agent Loop → Ranker → CSV + HTML Output

The scorer sends each company's data to the LLM with a structured prompt
that enforces differentiated scoring across a 1-10 range. Temperature is
set to 0.2 for consistent, reproducible output. The model returns pure JSON
which is parsed directly — no regex, no fragile string matching.

The pipeline is Claude API-ready. Swapping Groq for Anthropic requires
changing only the client initialization in scorer.py.

## What broke and how I fixed it

- Scraper returned 404: assumed wrong URL structure, fixed by fetching
  the real page and inspecting actual HTML tags and class names
- Model decommissioned: llama3-8b-8192 removed by Groq, switched to
  llama-3.3-70b-versatile per Groq deprecation docs
- Score clustering: all companies scored 9 because the source list was
  already curated top-tier startups — fixed by adding explicit score band
  criteria (9-10 / 7-8 / 5-6 / 3-4 / 1-2) and instructing the model
  to avoid giving more than 2 companies the same score

## Notes

- To scale beyond 10 companies, change max_companies in main.py
- The .env file must never be committed to GitHub — check .gitignore
- Groq free tier has rate limits — scorer.py includes a 0.5s delay per call
