# 📊 KPI PowerPoint Generator

[![CI](https://github.com/raghavhvr/kpi-ppt/actions/workflows/ci.yml/badge.svg)](https://github.com/raghavhvr/kpi-ppt/actions/workflows/ci.yml)
[![Monthly Report](https://github.com/raghavhvr/kpi-ppt/actions/workflows/monthly.yml/badge.svg)](https://github.com/raghavhvr/kpi-ppt/actions/workflows/monthly.yml)

AI-assisted tool that pulls **open economic indicators**, analyzes growth & trends, and generates automated **PowerPoint decks** with charts + narratives.  
Perfect for leadership reports and recurring dashboards.

---

## 🚀 Demo

### CLI
```powershell
python main.py --countries IN,US,GB --start 2000 --end 2024 --title "Global KPI Pack"
```

### Artifacts are saved to artifacts/reports/:
report_YYYYMMDD.pptx – auto-generated deck with charts + commentary

### Example Slide Content

Title: GDP Growth — India (2000–2024)
Line chart with YoY growth + 5-year CAGR annotated
Narrative paragraph summarizing growth and comparing countries

## 📊 Example Output

Generated chart (per indicator):

X-axis: Year
Y-axis: Value (GDP, population, inflation, etc.)
Multiple countries plotted, with legend

Narrative example:

“India’s GDP has grown at a 5.2% CAGR over the last 5 years, outpacing the UK but trailing the US. The sharpest acceleration occurred post-2010, with resilience during global downturns.”

## 🧰 Tech Stack

Data: World Bank API (requests + pandas)
Analysis: Pandas (YoY %, 5y CAGR calculations)
Visualization: Matplotlib (line charts)
Reports: python-pptx (multi-slide PPT export)
Automation: GitHub Actions (monthly scheduled run)

## 📦 Project Structure
```yaml
kpi-ppt/
├─ src/
│  ├─ wb.py          # fetch data from World Bank API
│  ├─ analysis.py    # YoY growth, CAGR, enrich dataset
│  ├─ charts.py      # matplotlib line charts per indicator
│  ├─ narrative.py   # generate text commentary
│  ├─ report.py      # assemble PowerPoint
│  └─ __init__.py
├─ artifacts/        # generated PPT reports
├─ main.py           # CLI entrypoint
├─ config.yaml       # configurable indicators/countries
├─ requirements.txt
├─ README.md
└─ .github/workflows/
   ├─ ci.yml         # lint + type checks + smoke
   └─ monthly.yml    # monthly automated PPT build + release
```

## ⚙️ Configuration Notes

Countries are passed as ISO2 codes (IN,US,GB).

Indicators configured in config.yaml (GDP, inflation, population, etc.).

Chart aesthetics (colors, DPI, layout) are in charts.py.

Narratives generated via simple heuristics (growth detection, CAGR summaries).

## 🗺️ Roadmap

 Add more indicators (CO₂, unemployment, literacy, etc.)

 Integrate LLM for richer narrative generation

 Export PDF version alongside PPT

 Build a Streamlit app for interactive indicator selection

 Enhance CI to publish thumbnails of key charts in releases

## 👨‍💻 Author

Portfolio project by Raghav
Part of the AI Automation Portfolio showcasing business-focused AI tools.