#!/usr/bin/env python3
"""
Build final 1000-question benchmark from 15K+ covered entries.
Prioritize: causal/prediction questions > sentiment > factual QA.
"""
import json, os, re, random, glob

random.seed(42)
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

COMPANY_MAP = {
    'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOG', 'alphabet': 'GOOG',
    'amazon': 'AMZN', 'meta platforms': 'META', 'facebook': 'META', 'intel': 'INTC',
    'qualcomm': 'QCOM', 'broadcom': 'AVGO', 'tsmc': 'TSM', 'asml': 'ASML',
    'texas instruments': 'TXN', 'jpmorgan': 'JPM', 'jp morgan': 'JPM',
    'bank of america': 'BAC', 'goldman sachs': 'GS', 'morgan stanley': 'MS',
    'wells fargo': 'WFC', 'tesla': 'TSLA', 'gamestop': 'GME', 'disney': 'DIS',
    'nvidia': 'NVDA', 'amd': 'AMD',
}
TICKERS = set(COMPANY_MAP.values())
ECON_KW = ['interest rate','inflation','gdp','unemployment','mortgage','recession',
           'federal reserve','monetary policy','fiscal policy','consumer price',
           'consumer sentiment','industrial production','durable goods',
           'jobless claims','treasury yield','bond yield','stock market',
           'economic growth','rate hike','rate cut','money supply',
           'aggregate demand','aggregate supply','exchange rate',
           'price level','labor market','business cycle','capital market']

def extract_coverage(text):
    tl = text.lower()
    tickers = []
    for name, t in COMPANY_MAP.items():
        if name in tl:
            tickers.append(t)
    for t in TICKERS:
        if re.search(rf'\b{t}\b', text):
            tickers.append(t)
    concepts = []
    for kw in ECON_KW:
        if kw in tl:
            concepts.append(kw)
    return list(set(tickers)), concepts[:5]

def get_text(entry):
    for key in ['question','prompt','input','text','premise','sentence','claim']:
        if entry.get(key) and isinstance(entry[key], str) and len(entry[key]) > 10:
            return entry[key]
    return ' '.join(str(v)[:200] for v in entry.values() if isinstance(v, str))[:500]

def get_gt(entry):
    for key in ['answer','output','label','target','ground_truth']:
        if entry.get(key) is not None:
            return entry[key]
    return None

# Priority tiers for source selection
TIER1_FILES = {  # Causal/prediction/decision - highest value
    "dellma_stock_questions.json": ("DeLLMa", "stock_decision", 120),
    "forecastbench_financial.json": ("ForecastBench", "prediction", 90),
    "futurex_past.json": ("FutureX", "prediction", 30),
    "flare_causal20.json": ("FLARE_Causal20", "causal_classification", 100),
    "flare_cd.json": ("FLARE_CD", "causal_detection", 45),
    "finben_fomc.json": ("FinBen_FOMC", "monetary_policy", 80),
    "stock_news_prediction.json": ("StockNews", "stock_prediction", 100),
    "flare_sm_acl.json": ("FLARE_SM", "stock_movement", 80),
}
TIER2_FILES = {  # Economics knowledge / financial reasoning
    "mmlu_econ.json": ("MMLU", "economics", 100),
    "flare_cfa.json": ("FLARE_CFA", "cfa_exam", 80),
    "econcausal.json": ("EconCausal", "economic_causality", 80),
    "fin_fact.json": ("FinFact", "fact_checking", 60),
    "finance_benchmark_mcq.json": ("FinMCQ", "finance_mcq", 60),
}
TIER3_FILES = {  # Financial QA / sentiment / other
    "financial_qa_10k.json": ("FinQA_10K", "financial_qa", 50),
    "finqa.json": ("FinQA", "financial_qa", 40),
    "financial_reasoning.json": ("FinReasoning", "financial_reasoning", 30),
    "flare_multifin.json": ("FLARE_MultiFin", "headline_classification", 20),
    "truthfulqa_econ.json": ("TruthfulQA", "truthful", 8),
    "bbh_causal.json": ("BBH", "causal_judgement", 10),
    "financebench.json": ("FinanceBench", "sec_filing_qa", 20),
    "tatqa.json": ("TAT_QA", "tabular_qa", 20),
    "ecare.json": ("eCARE", "causal_reasoning", 15),
}

all_selected = []

for tier_name, tier_files in [("TIER1", TIER1_FILES), ("TIER2", TIER2_FILES), ("TIER3", TIER3_FILES)]:
    print(f"\n=== {tier_name} ===")
    for fname, (source, category, quota) in tier_files.items():
        path = os.path.join(DATA, fname)
        if not os.path.exists(path):
            print(f"  {fname}: NOT FOUND")
            continue
        with open(path) as f:
            raw = json.load(f)

        # Special handling for DeLLMa
        if source == "DeLLMa":
            for q in raw:
                abel_stocks = [("GOOG" if s=="GOOGL" else s) for s in q["stocks"] if s.replace("L","") in TICKERS or s in TICKERS]
                if abel_stocks:
                    all_selected.append({
                        "source": source, "category": category,
                        "question": f"Invest $10K for one month: {' vs '.join(q['stocks'])}",
                        "ground_truth": q["ground_truth"],
                        "abel_tickers": abel_stocks, "abel_concepts": [],
                    })
            print(f"  {fname}: added {len([q for q in all_selected if q['source']==source])}")
            continue

        # General handling
        covered = []
        for entry in raw:
            text = get_text(entry)
            tickers, concepts = extract_coverage(text)
            if tickers or concepts:
                covered.append({
                    "source": source, "category": category,
                    "question": text[:400],
                    "ground_truth": get_gt(entry),
                    "abel_tickers": tickers, "abel_concepts": concepts,
                })

        # Sample up to quota
        if len(covered) > quota:
            sampled = random.sample(covered, quota)
        else:
            sampled = covered
        all_selected.extend(sampled)
        print(f"  {fname}: {len(covered)} covered, sampled {len(sampled)}")

# Trim to 1000
if len(all_selected) > 1000:
    all_selected = all_selected[:1000]

# Assign IDs
for i, q in enumerate(all_selected):
    q["eval_id"] = f"Q{i+1:04d}"

print(f"\n{'='*60}")
print(f"FINAL: {len(all_selected)} questions")
by_source = {}
for q in all_selected:
    s = q["source"]
    by_source[s] = by_source.get(s, 0) + 1
for s, n in sorted(by_source.items(), key=lambda x: -x[1]):
    print(f"  {s}: {n}")

# Count unique benchmarks
benchmarks = set(q["source"] for q in all_selected)
print(f"\nFrom {len(benchmarks)} distinct benchmarks")

out = os.path.join(DATA, "final_1000q.json")
with open(out, "w") as f:
    json.dump(all_selected, f, indent=1, ensure_ascii=False)
print(f"Saved to {out}")
