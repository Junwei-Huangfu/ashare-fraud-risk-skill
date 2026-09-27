"""Module 3: LLM interpretation — turn indicators and red flags into a structured risk report.

Works with any OpenAI-compatible API (DeepSeek, Qwen, OpenAI, Claude, ...).
Set LLM_API_KEY / LLM_BASE_URL / LLM_MODEL in a local .env file (never commit it).
Without a key, the script still saves the full prompt so it can be reviewed or pasted manually.
"""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"
COMPANIES = {"sh600518": "康美药业", "sz000538": "云南白药"}
PEER = {"sh600518": "sz000538", "sz000538": "sh600518"}
KEY_COLUMNS = ["营业收入(亿)", "净利润(亿)", "M_Score", "现金/总资产", "有息负债/总资产",
               "净现金(亿)", "财务费用/营业收入", "3年经营现金流/净利润", "存货增速-收入增速"]

SYSTEM_PROMPT = """你是一名资深的卖方财务分析师，专长是财务造假识别（forensic accounting）。
你的任务是基于给定的财务指标和规则引擎输出的红旗信号，撰写一份结构化的财务风险分析报告。

严格要求：
1. 只能使用提供的数据，不得编造任何数字、事件或新闻。
2. 每一个判断都必须引用具体年份和数值作为证据。
3. 区分“数据显示的异常”和“推测的可能原因”，推测部分要明确标注。
4. 语言专业、简洁，面向专业投资者。"""

USER_TEMPLATE = """请分析【{name}（{code}）】的财务风险，并与同行业可比公司【{peer_name}】对比。

## 目标公司年度指标
{target_table}

## 目标公司规则引擎红旗
{flags}

## 可比公司年度指标
{peer_table}

## 指标说明
- M_Score：Beneish 五变量模型，高于 -2.22 提示盈余操纵可能性较高
- 现金/总资产 与 有息负债/总资产 同时高于 20%：即“存贷双高”
- 净现金为正但 财务费用/营业收入 超过 1%：账面现金可能不真实
- 3年经营现金流/净利润 低于 0.5：利润缺乏现金支撑

## 报告结构（请用中文、Markdown 格式输出）
1. **结论与风险等级**（高/中/低，一句话理由）
2. **关键红旗**（逐条列出，每条附年份和数值证据）
3. **与可比公司对比**
4. **可能的造假手法推测**（明确标注为推测）
5. **建议的进一步核查程序**（例如函证、查阅附注中的受限资金等）
6. **分析局限性**（例如模型本身的适用范围、数据口径问题）"""


def build_prompt(code: str) -> str:
    target = pd.read_csv(PROCESSED_DIR / f"{code}_indicators.csv", index_col=0)
    peer = pd.read_csv(PROCESSED_DIR / f"{PEER[code]}_indicators.csv", index_col=0)
    flags = "\n".join(f"- {year}: {text}" for year, text in target["红旗"].fillna("").items() if text)
    return USER_TEMPLATE.format(
        name=COMPANIES[code], code=code, peer_name=COMPANIES[PEER[code]],
        target_table=target[KEY_COLUMNS].to_string(),
        flags=flags or "- 无",
        peer_table=peer[KEY_COLUMNS].to_string(),
    )


def call_llm(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["LLM_API_KEY"],
                    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"))
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        temperature=0.2,  # low temperature: we want consistent, evidence-based output
    )
    return response.choices[0].message.content


def run(code: str = "sh600518") -> None:
    load_dotenv(ROOT / ".env")
    REPORT_DIR.mkdir(exist_ok=True)
    prompt = build_prompt(code)
    (REPORT_DIR / f"{code}_prompt.md").write_text(SYSTEM_PROMPT + "\n\n---\n\n" + prompt, encoding="utf-8")

    if not os.getenv("LLM_API_KEY"):
        print("No LLM_API_KEY found. Prompt saved to reports/ — add a key to .env to generate the report.")
        return
    print(f"Calling LLM for {COMPANIES[code]} ...")
    report = call_llm(prompt)
    path = REPORT_DIR / f"{code}_report.md"
    path.write_text(report, encoding="utf-8")
    print(f"Report saved -> {path.relative_to(ROOT)}")


if __name__ == "__main__":
    for c in COMPANIES:
        run(c)