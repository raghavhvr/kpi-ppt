[![CI](https://github.com/raghavhvr/kpi-ppt/actions/workflows/ci.yml/badge.svg)](https://github.com/raghavhvr/kpi-ppt/actions/workflows/ci.yml)
[![Monthly Report](https://github.com/raghavhvr/kpi-ppt/actions/workflows/monthly.yml/badge.svg)](https://github.com/raghavhvr/kpi-ppt/actions/workflows/monthly.yml)

# Automated KPI Storytelling → Auto-PPT (Open Data)

Generates a polished PowerPoint summarizing key KPIs across countries with charts + auto-narrative. Data: World Bank Indicators API (WDI).

## Indicators (default)
- GDP (current US$) — `NY.GDP.MKTP.CD`
- Life expectancy at birth — `SP.DYN.LE00.IN`
- CO₂ emissions per capita — `EN.ATM.CO2E.PC`
- Renewable electricity output (%) — `EG.ELC.RNEW.ZS`

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python main.py --countries IN,US,GB --start 2000 --end 2024 --title "Global KPI Pack"