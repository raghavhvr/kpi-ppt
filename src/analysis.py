import pandas as pd

def enrich_growth(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Sort for stability
    df = df.sort_values(["indicator", "country", "year"])

    # Year-over-year growth
    df["yoy"] = (
        df.groupby(["indicator", "country"], observed=True)["value"]
          .pct_change(fill_method=None)
    )

    # CAGR over 5-year span
    def _cagr5(group: pd.DataFrame) -> pd.Series:
        vals = group["value"].reset_index(drop=True)
        years = group["year"].reset_index(drop=True)
        out = [None] * len(vals)
        for i in range(len(vals)):
            j = i - 5
            if j >= 0:
                v0, v1 = vals.iloc[j], vals.iloc[i]
                y0, y1 = years.iloc[j], years.iloc[i]
                if pd.notna(v0) and pd.notna(v1) and v0 != 0 and pd.notna(y0) and pd.notna(y1):
                    n = int(y1) - int(y0)
                    if n > 0:
                        out[i] = (v1 / v0) ** (1 / n) - 1
        return pd.Series(out, index=group.index)

    df["cagr_5y"] = (
        df.groupby(["indicator", "country"], observed=True, group_keys=False)
          .apply(_cagr5)
    )

    return df

def latest_snapshot(df: pd.DataFrame):
    latest_year = int(df["year"].max())
    latest = (
        df[df["year"] == latest_year]
        .groupby(["indicator", "country", "country_name"], observed=True, as_index=False)
        .agg(value=("value", "first"))
    )
    return latest, latest_year