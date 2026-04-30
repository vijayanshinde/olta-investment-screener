import os
from groq import Groq
from dotenv import load_dotenv
import json
import time

load_dotenv()

client = Groq(api_key=os.getenv("groq_api_key"))

def score_company(company: dict) -> dict:
    prompt = f"""
You are an investment analyst evaluating German startups for a venture investment fund.

Analyze this company and return a JSON object with exactly these fields:
- score: integer from 1 to 10 (investment attractiveness)
- rationale: one sentence explaining the score
- risk: one word risk level (Low / Medium / High)

Company data:
Name: {company['name']}
Description: {company['description']}
Location: {company['location']}
Founded: {company['founded']}
Funding: {company['funding']}
Size: {company['size']}
Stage: {company['stage']}

Scoring criteria (be strict and differentiated — avoid clustering scores):
- Score 9-10: Exceptional. Massive funding (500M+), cutting-edge sector (AI/Defense/DeepTech), Series C or later
- Score 7-8: Strong. Good funding (100M-500M), solid sector, Series A/B
- Score 5-6: Average. Moderate funding, established but not exciting sector
- Score 3-4: Below average. Low funding, high competition sector, or debt financing
- Score 1-2: Weak. Very early, minimal funding, or declining sector

You MUST spread scores across the full range. Do not give more than 2 companies the same score.

Return ONLY a valid JSON object, no explanation, no markdown.
Example: {{"score": 8, "rationale": "Strong AI focus with proven funding trajectory.", "risk": "Low"}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # free and fast on Groq
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # low temp = consistent scoring
        )

        raw = response.choices[0].message.content.strip()
        result = json.loads(raw)

        return {
            **company,
            "score": result.get("score", 0),
            "rationale": result.get("rationale", "N/A"),
            "risk": result.get("risk", "N/A"),
        }

    except json.JSONDecodeError:
        print(f"JSON parse error for {company['name']}, raw output: {raw}")
        return {**company, "score": 0, "rationale": "Parse error", "risk": "N/A"}

    except Exception as e:
        print(f"API error for {company['name']}: {e}")
        return {**company, "score": 0, "rationale": "API error", "risk": "N/A"}


def score_all(companies: list) -> list:
    scored = []
    for i, company in enumerate(companies):
        print(f"Scoring {i+1}/{len(companies)}: {company['name']}")
        result = score_company(company)
        scored.append(result)
        time.sleep(0.5)  # avoid hitting rate limits
    return scored