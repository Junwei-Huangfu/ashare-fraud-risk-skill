"""Module 4: Automated evaluation of LLM reports.

Two checks, both runnable without any extra API calls:
1. Risk-level accuracy: does the report's risk rating match the known label?
   (Kangmei = confirmed fraud -> 高; Yunnan Baiyao = no known fraud -> 低/中)
2. Number grounding: is every number quoted in the report present in the data
   the model was given? Ungrounded numbers are potential hallucinations.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"
COMPANIES = {"sh600518": "康美药业", "sz000538": "云南白药"}
EXPECTED = {"sh600518": {"高"}, "sz000538": {"低", "中"}}  # ground-truth labels

NUMBER = re.compile(r"-?\d+\.\d+")


def extract_risk_level(report: str) -> str:
    match = re.search(r"风险等级[\s*：:]*([高中低])", report)
    if not match:
        match = re.search(r"([高中低])风险", report)
    return match.group(1) if match else "未识别"


def grounding(report: str, source: str) -> tuple[int, list[str]]:
    """Return (number of quoted figures, list of figures not found in the source data).

    A figure counts as grounded if it matches a source value directly, or after the
    model converted a ratio into a percentage (e.g. 0.208 -> 20.8%).
    Section numbers such as "2.1" at the start of a line are ignored.
    """
    body = re.sub(r"(?m)^[\s#*]*\d+\.\d+(?=\s)", "", report)
    figures = set(NUMBER.findall(body))
    source_values = [float(v) for v in NUMBER.findall(source)]
    missing = []
    for f in sorted(figures):
        # a range like "0.025-0.033" is read as "-0.033", so compare absolute values too
        x = float(f)
        ok = any(abs(abs(x) - abs(v)) < 5e-4 or abs(abs(x) - abs(v) * 100) < 0.051 for v in source_values)
        if not ok:
            missing.append(f)
    return len(figures), missing


def run() -> None:
    lines = ["# Evaluation Results", "",
             "| Company | Expected | Predicted | Correct | Figures quoted | Grounded | Ungrounded figures |",
             "|---|---|---|---|---|---|---|"]
    for code, name in COMPANIES.items():
        report_path = REPORT_DIR / f"{code}_report.md"
        if not report_path.exists():
            print(f"Skip {name}: no report yet (run src/report.py first)")
            continue
        report = report_path.read_text(encoding="utf-8")
        source = (REPORT_DIR / f"{code}_prompt.md").read_text(encoding="utf-8")

        level = extract_risk_level(report)
        correct = "✅" if level in EXPECTED[code] else "❌"
        total, missing = grounding(report, source)
        rate = f"{(total - len(missing)) / total:.0%}" if total else "n/a"
        lines.append(f"| {name} | {'/'.join(sorted(EXPECTED[code]))} | {level} | {correct} "
                     f"| {total} | {rate} | {', '.join(missing) or '—'} |")
        print(f"{name}: risk={level} {correct} | grounded {rate} of {total} figures | ungrounded: {missing or 'none'}")

    out = REPORT_DIR / "evaluation.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    run()