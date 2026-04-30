import requests
from bs4 import BeautifulSoup

def scrape_startups(max_companies=20):
    url = "https://www.failory.com/startups/germany"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    companies = []

    # Each company has an h3 heading with a link
    headings = soup.find_all("h3")[:max_companies]

    for heading in headings:
        try:
            name = heading.get_text(strip=True)

            # Description is in the next <p> tag after heading
            description_tag = heading.find_next("p")
            description = description_tag.get_text(strip=True) if description_tag else "N/A"

            # Table rows contain metadata (HQ, Founded, Funding etc.)
            table = heading.find_next("table")
            metadata = {}
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) == 2:
                        key = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        metadata[key] = value

            companies.append({
                "name": name,
                "description": description,
                "location": metadata.get("Headquarters", "N/A"),
                "founded": metadata.get("Year Founded", "N/A"),
                "funding": metadata.get("Funding Amount", "N/A"),
                "size": metadata.get("Startup Size", "N/A"),
                "stage": metadata.get("Last Funding Status", "N/A"),
            })

        except Exception as e:
            print(f"Skipping entry due to error: {e}")
            continue

    print(f"Scraped {len(companies)} companies")
    return companies


if __name__ == "__main__":
    data = scrape_startups()
    for c in data:
        print(c)
        print("---")