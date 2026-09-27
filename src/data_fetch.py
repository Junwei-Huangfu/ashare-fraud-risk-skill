"""Module 1: Data collection — fetch A-share financial statements from Sina Finance via AKShare."""
import time
from pathlib import Path

import akshare as ak

# Case companies: Kangmei (fraud sample) vs Yunnan Baiyao (normal peer)
COMPANIES = {
    "sh600518": "康美药业",
    "sz000538": "云南白药",
}
STATEMENTS = ["资产负债表", "利润表", "现金流量表"]
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def fetch_all():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for code, name in COMPANIES.items():
        for statement in STATEMENTS:
            print(f"Fetching {name} ({code}) - {statement} ...")
            df = ak.stock_financial_report_sina(stock=code, symbol=statement)
            path = OUTPUT_DIR / f"{code}_{statement}.csv"
            df.to_csv(path, index=False, encoding="utf-8-sig")
            print(f"  Saved {len(df)} periods -> {path.name}")
            time.sleep(1)  # be polite to the data source


if __name__ == "__main__":
    fetch_all()