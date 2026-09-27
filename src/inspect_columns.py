"""Helper: find the exact column names we need in the raw statements."""
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
KEYWORDS = {
    "资产负债表": ["货币资金", "应收", "存货", "流动资产合计", "固定资产", "资产总计",
               "流动负债合计", "短期借款", "长期借款", "应付债券", "负债合计"],
    "利润表": ["营业", "销售费用", "管理费用", "财务费用", "利息", "净利润"],
    "现金流量表": ["经营活动产生的现金流量净额", "折旧"],
}

for statement, words in KEYWORDS.items():
    df = pd.read_csv(RAW_DIR / f"sh600518_{statement}.csv")
    print(f"\n===== {statement} ({len(df.columns)} columns) =====")
    print("Sample 报告日:", df["报告日"].head(3).tolist())
    for w in words:
        matches = [c for c in df.columns if w in c]
        print(f"{w}: {matches}")