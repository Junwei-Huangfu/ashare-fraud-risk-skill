"""Module 2: Ratio screening — Beneish M-Score (5-variable) + China-specific red flags.

Uses annual reports only. The 5-variable Beneish model is used because the data
source does not disclose depreciation, so DEPI cannot be computed.
M = -6.065 + 0.823*DSRI + 0.906*GMI + 0.593*AQI + 0.717*SGI + 7.770*TATA
A score above -2.22 suggests a higher likelihood of earnings manipulation.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"
COMPANIES = {"sh600518": "康美药业", "sz000538": "云南白药"}
M_THRESHOLD = -2.22


def load_annual(code: str) -> pd.DataFrame:
    """Merge the three statements into one table of annual (Dec 31) reports."""
    frames = []
    for statement in ["资产负债表", "利润表", "现金流量表"]:
        df = pd.read_csv(RAW_DIR / f"{code}_{statement}.csv")
        df["报告日"] = df["报告日"].astype(str)
        df = df[df["报告日"].str.endswith("1231")].set_index("报告日")
        frames.append(df)
    merged = frames[0].join(frames[1], rsuffix="_is").join(frames[2], rsuffix="_cf")
    merged.index = merged.index.str[:4].astype(int)
    return merged.sort_index()


def col(df: pd.DataFrame, *names: str) -> pd.Series:
    """Return the first available column, filling gaps with later fallbacks
    (e.g. 2018-19 reports merged receivables with notes receivable)."""
    result = pd.Series(np.nan, index=df.index)
    for n in names:
        if n in df.columns:
            result = result.fillna(pd.to_numeric(df[n], errors="coerce"))
    return result


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    sales = col(df, "营业收入", "营业总收入")
    cogs = col(df, "营业成本")
    ar = col(df, "应收账款", "应收票据及应收账款")
    ca = col(df, "流动资产合计")
    ppe = col(df, "固定资产净额", "固定资产及清理合计")
    ta = col(df, "资产总计")
    ni = col(df, "净利润")
    cfo = col(df, "经营活动产生的现金流量净额")
    cash = col(df, "货币资金")
    inventory = col(df, "存货")
    debt = col(df, "短期借款").fillna(0) + col(df, "长期借款").fillna(0) + col(df, "应付债券").fillna(0)
    fin_cost = col(df, "财务费用")

    gm = (sales - cogs) / sales
    aq = 1 - (ca + ppe) / ta

    out = pd.DataFrame(index=df.index)
    out["营业收入(亿)"] = sales / 1e8
    out["净利润(亿)"] = ni / 1e8
    # Beneish components
    out["DSRI"] = (ar / sales) / (ar / sales).shift(1)
    out["GMI"] = gm.shift(1) / gm
    out["AQI"] = aq / aq.shift(1)
    out["SGI"] = sales / sales.shift(1)
    out["TATA"] = (ni - cfo) / ta
    out["M_Score"] = (-6.065 + 0.823 * out["DSRI"] + 0.906 * out["GMI"]
                      + 0.593 * out["AQI"] + 0.717 * out["SGI"] + 7.770 * out["TATA"])
    # China-specific red flags
    out["现金/总资产"] = cash / ta
    out["有息负债/总资产"] = debt / ta
    out["净现金(亿)"] = (cash - debt) / 1e8
    out["财务费用(亿)"] = fin_cost / 1e8
    out["财务费用/营业收入"] = fin_cost / sales
    out["经营现金流/净利润"] = cfo / ni
    out["3年经营现金流/净利润"] = cfo.rolling(3).sum() / ni.rolling(3).sum()
    out["存货增速-收入增速"] = inventory.pct_change(fill_method=None) - sales.pct_change(fill_method=None)
    return out.round(3)


def red_flags(row: pd.Series) -> list[str]:
    flags = []
    if row["M_Score"] > M_THRESHOLD:
        flags.append(f"M-Score {row['M_Score']:.2f} above {M_THRESHOLD}")
    if row["现金/总资产"] > 0.2 and row["有息负债/总资产"] > 0.2:
        flags.append("存贷双高: large cash and large borrowings at the same time")
    if row["净现金(亿)"] > 0 and row["财务费用/营业收入"] > 0.01:
        flags.append("Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real")
    if row["3年经营现金流/净利润"] < 0.5:
        flags.append(f"3-year operating cash flow covers only {row['3年经营现金流/净利润']:.0%} of profit")
    if row["存货增速-收入增速"] > 0.2:
        flags.append("Inventory growing much faster than revenue")
    return flags


def run(start: int = 2012, end: int = 2020) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for code, name in COMPANIES.items():
        ind = compute_indicators(load_annual(code)).loc[start:end]
        ind["红旗"] = ind.apply(lambda r: "; ".join(red_flags(r)), axis=1)
        ind.to_csv(OUT_DIR / f"{code}_indicators.csv", encoding="utf-8-sig")
        results[name] = ind
        print(f"\n===== {name} ({code}) =====")
        print(ind[["M_Score", "现金/总资产", "有息负债/总资产", "净现金(亿)", "财务费用/营业收入", "3年经营现金流/净利润"]])
        print("Red-flag count by year:", ind["红旗"].apply(lambda s: len(s.split("; ")) if s else 0).to_dict())
    return results


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.unicode.east_asian_width", True)
    run()