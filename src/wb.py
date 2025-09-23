from __future__ import annotations
import requests, pandas as pd
from typing import List

BASE = "https://api.worldbank.org/v2"

def _fetch_indicator_country(indicator: str, country: str, start: int, end: int) -> pd.DataFrame:
    params = {"date": f"{start}:{end}", "format": "json", "per_page": 20000}
    r = requests.get(f"{BASE}/country/{country}/indicator/{indicator}", params=params, timeout=40)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        return pd.DataFrame(columns=["country","country_name","year","value","indicator"])
    rows = data[1]
    recs = []
    for row in rows:
        if row.get("date") is None: 
            continue
        recs.append({
            "country": row["country"]["id"],
            "country_name": row["country"]["value"],
            "year": int(row["date"]),
            "value": None if row["value"] is None else float(row["value"]),
            "indicator": indicator
        })
    return pd.DataFrame.from_records(recs)

def fetch(indicators: List[str], countries: List[str], start: int, end: int) -> pd.DataFrame:
    frames = []
    for ind in indicators:
        for c in countries:
            f = _fetch_indicator_country(ind, c, start, end)
            if not f.empty:
                frames.append(f)
    if not frames:
        return pd.DataFrame(columns=["country","country_name","year","value","indicator"])
    df = pd.concat(frames, ignore_index=True)
    return df.drop_duplicates()