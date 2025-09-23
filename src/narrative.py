import pandas as pd

def insights_text(latest: pd.DataFrame, latest_year: int, labels: dict) -> str:
    # Build 6–10 crisp narrative bullets
    lines = [f"Auto KPI Story — latest year {latest_year}."]
    # pick top 8 facts by normalized value (per indicator scale differs, so do per indicator)
    for ind, g in latest.groupby("indicator"):
        g2 = g.dropna(subset=["value"]).sort_values("value", ascending=False)
        if g2.empty: 
            continue
        top = g2.head(2)
        label = labels.get(ind, ind)
        facts = [f"{r['country_name']} {label}: {r['value']:,.2f}" for _, r in top.iterrows()]
        lines.append(f"{label}: " + " | ".join(facts))
    return "\n".join(lines)