from __future__ import annotations
import argparse, yaml
from pathlib import Path
from datetime import datetime, timezone

from src import wb, analysis
from src.charts import line_chart
from src.narrative import insights_text
from src.report import build_ppt

def run(cfg_path: str, cli):
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    title        = cli.title or cfg.get("title", "KPI Pack")
    countries    = (cli.countries.split(",") if cli.countries
                    else cfg.get("countries", ["IN","US","GB"]))
    start_year   = cli.start or cfg.get("start_year", 2000)
    end_year     = cli.end or cfg.get("end_year", datetime.utcnow().year-1)
    dt = datetime.now(timezone.utc).strftime("%Y%m%d")
    indicators   = (cli.indicators.split(",") if cli.indicators
                    else list(cfg.get("indicators", {}).keys()))
    labels       = cfg.get("indicators", {})
    artifacts    = Path(cfg.get("artifacts_dir", "artifacts"))
    charts_dir   = artifacts / "charts"
    reports_dir  = artifacts / "reports"

    # 1) Fetch
    raw = wb.fetch(indicators, countries, start_year, end_year)
    if raw.empty: 
        raise SystemExit("No data returned. Check indicators/countries/years.")

    # 2) Metrics
    df = analysis.enrich_growth(raw)
    latest, latest_year = analysis.latest_snapshot(df)

    # 3) Charts
    chart_specs = []
    for code in indicators:
        chart_path = line_chart(df, code, labels.get(code, code), charts_dir)
        chart_specs.append((code, chart_path, labels.get(code, code)))

    # 4) Narrative
    story = insights_text(latest, latest_year, labels)

    # 5) PPT
    dt = datetime.utcnow().strftime("%Y%m%d")
    out_ppt = build_ppt(chart_specs, story, str(reports_dir / f"report_{dt}.pptx"), title)
    print(f"Saved: {out_ppt}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--countries", help="Comma-separated ISO2 codes (e.g., IN,US,GB)")
    ap.add_argument("--indicators", help="Comma-separated indicator codes")
    ap.add_argument("--start", type=int, help="Start year")
    ap.add_argument("--end", type=int, help="End year")
    ap.add_argument("--title", help="Deck title")
    args = ap.parse_args()
    run(args.config, args)