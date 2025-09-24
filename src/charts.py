from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def line_chart(df: pd.DataFrame, indicator: str, label: str, outdir: str) -> str:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    sub = df[df["indicator"] == indicator].dropna(subset=["value"])
    lines_plotted = 0
    for country, g in sub.groupby("country", observed=True):
        if not g.empty:
            plt.plot(g["year"], g["value"], label=str(country))
            lines_plotted += 1

    plt.xlabel("Year")
    plt.ylabel(label)
    plt.title(label)
    if lines_plotted > 0:
        plt.legend()

    fp = out / f"{indicator}.png"
    plt.tight_layout()
    plt.savefig(fp, dpi=180)
    plt.close()
    return str(fp)