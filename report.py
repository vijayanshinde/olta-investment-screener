import pandas as pd

def generate_html(csv_path="ranked_companies.csv", output_path="dashboard.html"):
    df = pd.read_csv(csv_path)

    # Clean up name numbering (e.g. "1.DeepL" -> "DeepL")
    df["name"] = df["name"].str.replace(r"^\d+\.", "", regex=True).str.strip()

    # Color map for risk
    risk_colors = {"Low": "#00c896", "Medium": "#f5a623", "High": "#e8445a"}
    risk_bg = {"Low": "#0a2e22", "Medium": "#2e1f00", "High": "#2e0a10"}

    # Build company cards
    cards_html = ""
    for i, row in df.iterrows():
        rank = i + 1
        score = int(row["score"])
        risk = str(row["risk"])
        name = str(row["name"])
        rationale = str(row["rationale"])
        location = str(row["location"]).replace(", Germany", "")
        founded = str(row["founded"])
        funding = str(row["funding"])
        stage = str(row["stage"])
        industry = str(row.get("size", ""))

        risk_color = risk_colors.get(risk, "#aaa")
        risk_bg_color = risk_bg.get(risk, "#111")

        # Score bar width
        bar_width = score * 10

        # Top 3 get a gold/silver/bronze accent
        rank_accent = ""
        if rank == 1:
            rank_accent = "card--gold"
        elif rank == 2:
            rank_accent = "card--silver"
        elif rank == 3:
            rank_accent = "card--bronze"

        cards_html += f"""
        <div class="card {rank_accent}" style="animation-delay: {i * 0.07}s">
            <div class="card-header">
                <div class="rank-badge">#{rank}</div>
                <div class="company-name">{name}</div>
                <div class="risk-badge" style="color:{risk_color}; background:{risk_bg_color};">{risk} Risk</div>
            </div>
            <div class="score-row">
                <span class="score-label">Investment Score</span>
                <div class="score-bar-wrap">
                    <div class="score-bar" style="width:{bar_width}%; background: linear-gradient(90deg, {risk_color}88, {risk_color});"></div>
                </div>
                <span class="score-num">{score}<span class="score-denom">/10</span></span>
            </div>
            <div class="meta-row">
                <span class="meta-item">📍 {location}</span>
                <span class="meta-item">📅 Founded {founded}</span>
                <span class="meta-item">💰 {funding}</span>
                <span class="meta-item">🚀 {stage}</span>
            </div>
            <div class="rationale">"{rationale}"</div>
        </div>
        """

    # Summary stats
    avg_score = round(df["score"].mean(), 1)
    top_company = df.iloc[0]["name"]
    high_risk_count = len(df[df["risk"] == "High"])
    low_risk_count = len(df[df["risk"] == "Low"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OLTA Investment Screener</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg: #080c10;
    --surface: #0e1318;
    --surface2: #141a21;
    --border: #1e2830;
    --text: #e8edf2;
    --muted: #5a6a78;
    --accent: #00c896;
    --gold: #f5c842;
    --silver: #a0b0c0;
    --bronze: #c87840;
  }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* Background grid */
  body::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.4;
    pointer-events: none;
    z-index: 0;
  }}

  .wrapper {{
    position: relative;
    z-index: 1;
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 24px 80px;
  }}

  /* Header */
  .header {{
    margin-bottom: 48px;
    animation: fadeDown 0.6s ease both;
  }}

  .header-tag {{
    font-size: 11px;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 12px;
  }}

  .header h1 {{
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: var(--text);
  }}

  .header h1 span {{
    color: var(--accent);
  }}

  .header-sub {{
    margin-top: 10px;
    font-size: 13px;
    color: var(--muted);
  }}

  /* Stats bar */
  .stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 36px;
    animation: fadeDown 0.6s 0.1s ease both;
  }}

  .stat {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
  }}

  .stat-val {{
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
  }}

  .stat-label {{
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
  }}

  /* Cards */
  .cards {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    opacity: 0;
    animation: fadeUp 0.5s ease forwards;
    transition: border-color 0.2s, transform 0.2s;
  }}

  .card:hover {{
    border-color: #2e3d4d;
    transform: translateY(-2px);
  }}

  .card--gold {{ border-left: 3px solid var(--gold); }}
  .card--silver {{ border-left: 3px solid var(--silver); }}
  .card--bronze {{ border-left: 3px solid var(--bronze); }}

  .card-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
  }}

  .rank-badge {{
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
    min-width: 28px;
  }}

  .company-name {{
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    flex: 1;
  }}

  .risk-badge {{
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid currentColor;
  }}

  .score-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }}

  .score-label {{
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    min-width: 110px;
  }}

  .score-bar-wrap {{
    flex: 1;
    height: 5px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
  }}

  .score-bar {{
    height: 100%;
    border-radius: 3px;
    transition: width 1s ease;
  }}

  .score-num {{
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    min-width: 36px;
    text-align: right;
  }}

  .score-denom {{
    font-size: 0.65rem;
    color: var(--muted);
    font-weight: 400;
  }}

  .meta-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
    margin-bottom: 12px;
  }}

  .meta-item {{
    font-size: 11px;
    color: var(--muted);
  }}

  .rationale {{
    font-size: 12px;
    color: #7a8c9a;
    font-style: italic;
    line-height: 1.5;
    border-top: 1px solid var(--border);
    padding-top: 10px;
  }}

  .footer {{
    margin-top: 48px;
    text-align: center;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.1em;
    animation: fadeDown 0.6s 0.3s ease both;
  }}

  @keyframes fadeDown {{
    from {{ opacity: 0; transform: translateY(-12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  @media (max-width: 600px) {{
    .stats {{ grid-template-columns: repeat(2, 1fr); }}
    .score-label {{ min-width: 80px; font-size: 9px; }}
  }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <div class="header-tag">Agentic AI Pipeline · OLTA Investments</div>
    <h1>German Startup<br><span>Investment Screener</span></h1>
    <div class="header-sub">Scraped → Scored → Ranked · {len(df)} companies analyzed</div>
  </div>

  <div class="stats">
    <div class="stat">
      <div class="stat-val">{len(df)}</div>
      <div class="stat-label">Companies</div>
    </div>
    <div class="stat">
      <div class="stat-val">{avg_score}</div>
      <div class="stat-label">Avg Score</div>
    </div>
    <div class="stat">
      <div class="stat-val">{low_risk_count}</div>
      <div class="stat-label">Low Risk</div>
    </div>
    <div class="stat">
      <div class="stat-val">{high_risk_count}</div>
      <div class="stat-label">High Risk</div>
    </div>
  </div>

  <div class="cards">
    {cards_html}
  </div>

  <div class="footer">
    OLTA Investment Screener · Powered by Groq LLM · Data: Failory.com
  </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard saved to {output_path} — open it in your browser")
