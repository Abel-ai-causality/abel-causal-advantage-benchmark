#!/usr/bin/env python3
"""
Build 1000-question evaluation set from all available benchmarks.
Uses the 3 validated flip patterns from the 30-question manual test.

Flip Pattern A: Stock decision with structural insight (parents reveal risk)
Flip Pattern B: Macro prediction with Markov blanket + web context
Flip Pattern C: Financial sentiment where observe direction provides signal
"""
import json, os, re, random, subprocess, time

random.seed(42)
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")
SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"

ABEL_TICKERS = {
    "AAPL","MSFT","GOOG","GOOGL","AMZN","META","INTC","QCOM","AVGO",
    "TSM","ASML","TXN","JPM","BAC","GS","MS","WFC","TSLA",
    "GME","DIS","LI","NDAQ",
}
ABEL_MACRO_KW = {
    "treasuryRateYear10": ["10-year treasury", "10 year treasury", "long-term bond yield", "treasury yield"],
    "federalFunds": ["federal funds rate", "fed funds", "overnight rate", "policy rate"],
    "CPI": ["consumer price index", "cpi "],
    "inflationRate": ["inflation rate", "price inflation", "inflation expect"],
    "GDP": [" gdp ", "gross domestic product", "economic growth rate", "output growth"],
    "realGDP": ["real gdp", "real output"],
    "unemploymentRate": ["unemployment rate", "unemployment level", "jobless rate"],
    "30YearFixedRateMortgageAverage": ["mortgage rate", "30-year mortgage", "housing loan rate", "home loan rate"],
    "15YearFixedRateMortgageAverage": ["15-year mortgage"],
    "consumerSentiment": ["consumer sentiment", "consumer confidence", "consumer spending index"],
    "durableGoods": ["durable goods", "durable orders", "manufacturing orders"],
    "initialClaims": ["initial claims", "jobless claims", "unemployment claims", "weekly claims"],
    "industrialProductionTotalIndex": ["industrial production", "factory output", "manufacturing index"],
}

def load_json(fname):
    path = os.path.join(DATA, fname)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def extract_tickers(text):
    found = []
    for t in ABEL_TICKERS:
        if re.search(rf'\b{t}\b', text):
            found.append(t)
    return found

def extract_macro(text):
    text_l = text.lower()
    found = []
    for node, kws in ABEL_MACRO_KW.items():
        for kw in kws:
            if kw in text_l:
                found.append(node)
                break
    return list(set(found))


# ============================================================
# LOAD ALL BENCHMARKS
# ============================================================
print("Loading all benchmarks...")

all_candidates = []

# 1. DeLLMa (120 stock decision questions)
dellma = load_json("dellma_stock_questions.json")
for q in dellma:
    abel_stocks = [("GOOG" if s=="GOOGL" else s) for s in q["stocks"] if (s in ABEL_TICKERS or s.replace("L","") in ABEL_TICKERS)]
    all_candidates.append({
        "source": "DeLLMa", "category": "stock_decision",
        "question": q["prompt"][:300],
        "text_for_matching": " ".join(q["stocks"]),
        "ground_truth": q["ground_truth"],
        "gt_detail": q.get("ground_truth_return_pct"),
        "stocks": q["stocks"],
        "abel_tickers": abel_stocks,
        "abel_macros": [],
        "flip_pattern": "A" if abel_stocks else None,
    })

# 2. ForecastBench
fb = load_json("forecastbench_financial.json")
for q in fb:
    text = q.get("question", "") + " " + q.get("background", "")
    tickers = []
    macros = []
    if q.get("data_source") == "yfinance":
        m = re.match(r"Will (\w+)'s", q.get("question", ""))
        if m and m.group(1) in ABEL_TICKERS:
            tickers = [m.group(1)]
    macros = extract_macro(text)
    pattern = None
    if tickers:
        pattern = "C"  # sentiment/direction with observe
    elif macros:
        pattern = "B"  # macro with blanket
    if pattern:
        all_candidates.append({
            "source": "ForecastBench", "category": q.get("data_source", "unknown"),
            "question": q.get("question", "")[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer"),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": pattern,
        })

# 3. FutureX
futurex = load_json("futurex_past.json")
for q in futurex:
    text = q["title"] + " " + q["prompt"]
    tickers = extract_tickers(text)
    macros = extract_macro(text)
    # Filter noise
    noise = ["kings", "knights", "oscars", "grammy", "super bowl", "nfl",
             "nba", "ufc", "uefa", "f1", "soccer", "movie", "book", "song",
             "president", "election", "traded by", "rangers", "puzzle",
             "audio drama", "猫耳", "anime", "temperature", "AFCON"]
    if any(n in text.lower() for n in noise):
        continue
    pattern = None
    if tickers:
        pattern = "A"
    elif macros:
        pattern = "B"
    if pattern:
        all_candidates.append({
            "source": "FutureX", "category": "prediction",
            "question": q["prompt"][:300],
            "title": q["title"],
            "text_for_matching": text[:500],
            "ground_truth": q["ground_truth"],
            "level": q["level"],
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": pattern,
        })

# 4. MMLU economics
mmlu = load_json("mmlu_econ.json")
for q in mmlu:
    text = q.get("question", "") + " " + " ".join(str(c) for c in q.get("choices", []))
    macros = extract_macro(text)
    tickers = extract_tickers(text)
    if macros or tickers:
        all_candidates.append({
            "source": "MMLU", "category": q.get("subset", "economics"),
            "question": q.get("question", "")[:300],
            "choices": q.get("choices", []),
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer"),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "B" if macros else "C",
        })

# 5. FLARE FPB (financial sentiment)
fpb = load_json("flare_fpb.json")
for q in fpb:
    text = q.get("text", q.get("input", ""))
    tickers = extract_tickers(text)
    macros = extract_macro(text)
    if tickers:
        all_candidates.append({
            "source": "FLARE_FPB", "category": "sentiment",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("label", q.get("output", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "C",
        })

# 6. FLARE FiQA
fiqa = load_json("flare_fiqa.json")
for q in fiqa:
    text = q.get("text", q.get("input", ""))
    tickers = extract_tickers(text)
    macros = extract_macro(text)
    if tickers or macros:
        all_candidates.append({
            "source": "FLARE_FiQA", "category": "sentiment",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("label", q.get("output", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "C" if tickers else "B",
        })

# 7. FLARE Headlines
headlines = load_json("flare_headlines.json")
for q in headlines:
    text = q.get("text", q.get("input", ""))
    tickers = extract_tickers(text)
    macros = extract_macro(text)
    if tickers or macros:
        all_candidates.append({
            "source": "FLARE_Headlines", "category": "headlines",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("label", q.get("output", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "C" if tickers else "B",
        })

# 8. FinQA
finqa = load_json("finqa.json")
for q in finqa:
    text = q.get("question", q.get("input", "")) + " " + q.get("context", "")
    tickers = extract_tickers(text)
    macros = extract_macro(text)
    if macros:
        all_candidates.append({
            "source": "FinQA", "category": "financial_qa",
            "question": q.get("question", q.get("input", ""))[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer", q.get("output", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "B",
        })

# 9. BBH Causal
bbh = load_json("bbh_causal.json")
for q in bbh:
    text = q.get("question", q.get("input", ""))
    macros = extract_macro(text)
    tickers = extract_tickers(text)
    if macros or tickers:
        all_candidates.append({
            "source": "BBH", "category": "causal_judgement",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer", q.get("target", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "B",
        })

# 10. TruthfulQA
tqa = load_json("truthfulqa_econ.json")
for q in tqa:
    text = q.get("question", "")
    macros = extract_macro(text)
    tickers = extract_tickers(text)
    if macros or tickers:
        all_candidates.append({
            "source": "TruthfulQA", "category": "truthful",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("labels", ""),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "B",
        })

# 11. eCARE
ecare = load_json("ecare.json")
for q in ecare:
    text = q.get("premise", "") + " " + q.get("hypothesis1", "") + " " + q.get("hypothesis2", "")
    macros = extract_macro(text)
    if macros:
        all_candidates.append({
            "source": "eCARE", "category": "causal_explanation",
            "question": q.get("premise", "")[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer", q.get("label", "")),
            "abel_tickers": [],
            "abel_macros": macros,
            "flip_pattern": "B",
        })

# 12. ConvFinQA
convfin = load_json("convfinqa.json")
for q in convfin:
    text = q.get("question", q.get("input", ""))
    macros = extract_macro(text)
    tickers = extract_tickers(text)
    if macros:
        all_candidates.append({
            "source": "ConvFinQA", "category": "financial_qa",
            "question": text[:300],
            "text_for_matching": text[:500],
            "ground_truth": q.get("answer", q.get("output", "")),
            "abel_tickers": tickers,
            "abel_macros": macros,
            "flip_pattern": "B",
        })

# ============================================================
# FILTER AND SELECT 1000
# ============================================================
print(f"\nTotal candidates with Abel coverage: {len(all_candidates)}")

by_source = {}
by_pattern = {}
for q in all_candidates:
    s = q["source"]
    p = q.get("flip_pattern", "?")
    by_source[s] = by_source.get(s, 0) + 1
    by_pattern[p] = by_pattern.get(p, 0) + 1

print("\nBy source:")
for s, n in sorted(by_source.items(), key=lambda x: -x[1]):
    print(f"  {s}: {n}")
print("\nBy flip pattern:")
for p, n in sorted(by_pattern.items(), key=lambda x: -x[1]):
    print(f"  Pattern {p}: {n}")

# Select 1000 with diversity
selected = []

# Take ALL from small sources first
for source in ["DeLLMa", "ForecastBench", "FutureX", "TruthfulQA", "BBH"]:
    src_qs = [q for q in all_candidates if q["source"] == source]
    selected.extend(src_qs)
    print(f"  Added all {len(src_qs)} from {source}")

remaining = 1000 - len(selected)
print(f"\nAfter small sources: {len(selected)}, need {remaining} more")

# Fill from larger sources proportionally
large_sources = ["MMLU", "FLARE_FPB", "FLARE_FiQA", "FLARE_Headlines", "FinQA", "ConvFinQA", "eCARE"]
large_pool = [q for q in all_candidates if q["source"] in large_sources]
if len(large_pool) > remaining:
    # Proportional sampling
    for source in large_sources:
        src_qs = [q for q in all_candidates if q["source"] == source]
        n_take = max(1, int(remaining * len(src_qs) / len(large_pool)))
        sample = random.sample(src_qs, min(n_take, len(src_qs)))
        selected.extend(sample)
        print(f"  Sampled {len(sample)} from {source}")
else:
    selected.extend(large_pool)

# Trim to exactly 1000
if len(selected) > 1000:
    selected = selected[:1000]
elif len(selected) < 1000:
    # Pad from remaining pool
    used_ids = set(id(q) for q in selected)
    unused = [q for q in all_candidates if id(q) not in used_ids]
    selected.extend(random.sample(unused, min(1000 - len(selected), len(unused))))

print(f"\nFinal selection: {len(selected)} questions")

# Final breakdown
final_sources = {}
final_patterns = {}
for q in selected:
    s = q["source"]
    p = q.get("flip_pattern", "?")
    final_sources[s] = final_sources.get(s, 0) + 1
    final_patterns[p] = final_patterns.get(p, 0) + 1

print("\nFinal by source:")
for s, n in sorted(final_sources.items(), key=lambda x: -x[1]):
    print(f"  {s}: {n}")
print("\nFinal by pattern:")
for p, n in sorted(final_patterns.items(), key=lambda x: -x[1]):
    print(f"  Pattern {p}: {n}")

# Save
out = os.path.join(DATA, "eval_1000q.json")
# Strip large fields
for i, q in enumerate(selected):
    q["eval_id"] = f"Q{i+1:04d}"
    q.pop("text_for_matching", None)
with open(out, "w") as f:
    json.dump(selected, f, indent=1, ensure_ascii=False)
print(f"\nSaved to {out}")
