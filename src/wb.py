from __future__ import annotations

from typing import Dict, List

import pandas as pd
import requests

BASE = "https://api.worldbank.org/v2"


def _encode_params(d: Dict[str, object]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple, set)):
            out[k] = ",".join(map(str, v))
        else:
            out[k] = str(v)
    return out


def _fetch_indicator_country(indicator: str, country: str, start: int, end: int) -> pd.DataFrame:
    params = {"date": f"{start}:{end}", "format": "json", "per_page": 20000}
    r = requests.get(
        f"{BASE}/country/{country}/indicator/{indicator}",
        params=_encode_params(params),  # <-- strictly typed params
        timeout=40,
    )
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        return pd.DataFrame(columns=["country", "country_name", "year", "value", "indicator"])

    rows = data[1]
    recs = []
    for row in rows:
        if row.get("date") is None:
            continue
        recs.append(
            {
                "country": row["country"]["id"],
                "country_name": row["country"]["value"],
                "year": int(row["date"]),
                "value": None if row["value"] is None else float(row["value"]),
                "indicator": indicator,
            }
        )
    return pd.DataFrame.from_records(recs)


def fetch(indicators: List[str], countries: List[str], start: int, end: int) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for ind in indicators:
        for c in countries:
            f = _fetch_indicator_country(ind, c, start, end)
            if not f.empty:
                frames.append(f)
    if not frames:
        return pd.DataFrame(columns=["country", "country_name", "year", "value", "indicator"])
    df = pd.concat(frames, ignore_index=True)
    return df.drop_duplicates()