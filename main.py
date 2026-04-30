import pandas as pd
from scraper import scrape_startups
from scorer import score_all
from report import generate_html          

def main():
    print("=== Step 1: Scraping companies ===")
    companies = scrape_startups(max_companies=10)

    if not companies:
        print("No companies scraped. Exiting.")
        return

    print(f"\n=== Step 2: Scoring {len(companies)} companies via Groq ===")
    scored = score_all(companies)

    print("\n=== Step 3: Ranking and saving output ===")
    df = pd.DataFrame(scored)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df.index += 1

    output_path = "ranked_companies.csv"
    df.to_csv(output_path, index_label="rank")

    generate_html()                        

    print(f"\nDone. Results saved to {output_path}")
    print("\n--- Top 5 ---")
    print(df[["name", "score", "risk", "rationale"]].head(5).to_string())

if __name__ == "__main__":
    main()
