#!/usr/bin/env python3
"""
V2: Expanded entity matching (company names + broad econ terms).
Goal: find 1000+ questions from existing benchmarks with Abel coverage.
"""
import json, os, re, random

random.seed(42)
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

# EXPANDED matching: company names + tickers + broad econ terms
COMPANY_MAP = {
    # Company name -> Abel ticker
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOG", "alphabet": "GOOG",
    "amazon": "AMZN", "meta": "META", "facebook": "META",
    "intel": "INTC", "qualcomm": "QCOM", "broadcom": "AVGO",
    "tsmc": "TSM", "asml": "ASML", "texas instruments": "TXN",
    "jpmorgan": "JPM", "jp morgan": "JPM", "bank of america": "BAC",
    "goldman sachs": "GS", "goldman": "GS", "morgan stanley": "MS",
    "wells fargo": "WFC", "citigroup": "C", "citibank": "C",
    "tesla": "TSLA", "gamestop": "GME", "disney": "DIS",
    "nvidia": "NVDA",  # exists but sparse
}

TICKER_SET = set(COMPANY_MAP.values()) | {
    "AAPL","MSFT","GOOG","GOOGL","AMZN","META","INTC","QCOM","AVGO",
    "TSM","ASML","TXN","JPM","BAC","GS","MS","WFC","TSLA","GME","DIS",
}

# Broader economic concept matching
ECON_CONCEPTS = {
    "interest_rate": ["interest rate", "interest-rate", "rate hike", "rate cut", "monetary policy",
                      "fed rate", "federal reserve", "central bank", "tightening", "easing",
                      "discount rate", "prime rate", "fed fund", "federal fund", "basis point"],
    "inflation": ["inflation", "deflation", "price level", "price stability", "cpi",
                  "consumer price", "cost of living", "purchasing power", "stagflation"],
    "gdp_growth": ["gdp", "gross domestic product", "economic growth", "economic output",
                   "recession", "expansion", "business cycle", "economic contraction",
                   "economic recovery", "gdp growth"],
    "unemployment": ["unemployment", "employment rate", "jobless", "labor market",
                     "job market", "nonfarm payroll", "labor force", "hiring",
                     "layoff", "job loss", "workforce"],
    "housing": ["mortgage", "housing market", "real estate", "home price",
                "housing start", "home sale", "property market"],
    "trade": ["trade deficit", "trade surplus", "tariff", "import", "export",
              "trade war", "trade balance", "current account"],
    "fiscal": ["fiscal policy", "government spending", "tax cut", "tax hike",
               "budget deficit", "national debt", "government debt", "stimulus"],
    "market": ["stock market", "equity market", "bull market", "bear market",
               "market crash", "market rally", "dow jones", "s&p 500", "nasdaq",
               "market capitalization", "stock exchange"],
    "banking": ["banking", "bank lending", "credit", "loan", "deposit",
                "banking sector", "financial sector", "bank failure", "liquidity"],
    "sentiment": ["consumer sentiment", "consumer confidence", "business confidence",
                  "investor sentiment", "market sentiment"],
    "manufacturing": ["industrial production", "manufacturing", "factory output",
                      "pmi", "purchasing manager", "durable goods", "supply chain"],
}

# Map concept -> Abel macro node
CONCEPT_TO_NODE = {
    "interest_rate": "federalFunds",
    "inflation": "inflationRate",
    "gdp_growth": "GDP",
    "unemployment": "unemploymentRate",
    "housing": "30YearFixedRateMortgageAverage",
    "sentiment": "consumerSentiment",
    "manufacturing": "industrialProductionTotalIndex",
    "banking": "federalFunds",
    "market": "treasuryRateYear10",
    "fiscal": "GDP",
    "trade": "GDP",
}


def extract_entities(text):
    """Extract Abel-covered entities from text using expanded matching."""
    text_l = text.lower()
    tickers = set()
    macros = set()

    # Ticker matching (word boundary)
    for t in TICKER_SET:
        if re.search(rf'\b{t}\b', text):
            tickers.add(t)

    # Company name matching
    for name, ticker in COMPANY_MAP.items():
        if name in text_l:
            tickers.add(ticker)

    # Economic concept matching
    for concept, keywords in ECON_CONCEPTS.items():
        for kw in keywords:
            if kw in text_l:
                node = CONCEPT_TO_NODE.get(concept)
                if node:
                    macros.add(node)
                macros.add(concept)  # also store the concept name
                break

    return list(tickers), list(macros)


def load_and_tag(fname, source, get_text, get_gt, category="general"):
    """Load a JSON file and tag questions with Abel coverage."""
    data = []
    path = os.path.join(DATA, fname)
    if not os.path.exists(path):
        return data
    with open(path) as f:
        raw = json.load(f)
    for q in raw:
        text = get_text(q)
        gt = get_gt(q)
        if not text:
            continue
        tickers, macros = extract_entities(text)
        if tickers or macros:
            data.append({
                "source": source, "category": category,
                "question": text[:400],
                "ground_truth": gt,
                "abel_tickers": tickers,
                "abel_macros": macros,
                "has_ticker": len(tickers) > 0,
                "has_macro": len([m for m in macros if m in CONCEPT_TO_NODE.values()]) > 0,
                "has_concept": len(macros) > 0,
            })
    return data


print("Loading and tagging all benchmarks with EXPANDED matching...\n")

all_q = []

# DeLLMa
dellma = []
for q in (json.load(open(os.path.join(DATA, "dellma_stock_questions.json"))) if os.path.exists(os.path.join(DATA, "dellma_stock_questions.json")) else []):
    abel_stocks = [("GOOG" if s=="GOOGL" else s) for s in q["stocks"] if (s in TICKER_SET or s.replace("L","") in TICKER_SET)]
    dellma.append({
        "source": "DeLLMa", "category": "stock_decision",
        "question": f"Invest $10K: choose between {', '.join(q['stocks'])}",
        "ground_truth": q["ground_truth"],
        "abel_tickers": abel_stocks, "abel_macros": [],
        "has_ticker": bool(abel_stocks), "has_macro": False, "has_concept": False,
        "stocks": q["stocks"], "gt_return": q.get("ground_truth_return_pct"),
    })
all_q.extend(dellma)

# ForecastBench
all_q.extend(load_and_tag("forecastbench_financial.json", "ForecastBench",
    lambda q: q.get("question","") + " " + q.get("background",""),
    lambda q: q.get("answer"), "prediction"))

# FutureX (pre-filter noise)
futurex_raw = json.load(open(os.path.join(DATA, "futurex_past.json"))) if os.path.exists(os.path.join(DATA, "futurex_past.json")) else []
noise_kw = ["kings","knights","oscars","grammy","super bowl","nfl","nba","ufc","uefa",
            "soccer","movie","book","song","president","election","puzzle","anime","猫耳","audio drama"]
for q in futurex_raw:
    text = q["title"] + " " + q["prompt"]
    if any(n in text.lower() for n in noise_kw):
        continue
    tickers, macros = extract_entities(text)
    if tickers or macros:
        all_q.append({
            "source": "FutureX", "category": "prediction",
            "question": q["prompt"][:400], "title": q["title"],
            "ground_truth": q["ground_truth"], "level": q["level"],
            "abel_tickers": tickers, "abel_macros": macros,
            "has_ticker": bool(tickers), "has_macro": bool(macros), "has_concept": bool(macros),
        })

# MMLU
all_q.extend(load_and_tag("mmlu_econ.json", "MMLU",
    lambda q: q.get("question","") + " " + " ".join(str(c) for c in q.get("choices",[])),
    lambda q: q.get("answer"), "economics"))

# FLARE FPB
all_q.extend(load_and_tag("flare_fpb.json", "FLARE_FPB",
    lambda q: q.get("text", q.get("input","")),
    lambda q: q.get("label", q.get("output","")), "sentiment"))

# FLARE FiQA
all_q.extend(load_and_tag("flare_fiqa.json", "FLARE_FiQA",
    lambda q: q.get("text", q.get("input","")),
    lambda q: q.get("label", q.get("output","")), "sentiment"))

# FLARE Headlines
all_q.extend(load_and_tag("flare_headlines.json", "FLARE_Headlines",
    lambda q: q.get("text", q.get("input","")),
    lambda q: q.get("label", q.get("output","")), "headlines"))

# FinQA
all_q.extend(load_and_tag("finqa.json", "FinQA",
    lambda q: q.get("question", q.get("input","")) + " " + str(q.get("context", q.get("text","")))[:200],
    lambda q: q.get("answer", q.get("output","")), "financial_qa"))

# ConvFinQA
all_q.extend(load_and_tag("convfinqa.json", "ConvFinQA",
    lambda q: q.get("question", q.get("input","")),
    lambda q: q.get("answer", q.get("output","")), "financial_qa"))

# TruthfulQA
all_q.extend(load_and_tag("truthfulqa_econ.json", "TruthfulQA",
    lambda q: q.get("question",""),
    lambda q: q.get("labels",""), "truthful"))

# BBH causal
all_q.extend(load_and_tag("bbh_causal.json", "BBH",
    lambda q: q.get("question", q.get("input","")),
    lambda q: q.get("answer", q.get("target","")), "causal"))

# eCARE
all_q.extend(load_and_tag("ecare.json", "eCARE",
    lambda q: q.get("premise","") + " " + q.get("hypothesis1","") + " " + q.get("hypothesis2",""),
    lambda q: q.get("answer", q.get("label","")), "causal"))

# ============================================================
# SUMMARY
# ============================================================
print(f"Total with Abel coverage (expanded): {len(all_q)}")

by_source = {}
for q in all_q:
    s = q["source"]
    by_source[s] = by_source.get(s, 0) + 1
for s, n in sorted(by_source.items(), key=lambda x: -x[1]):
    print(f"  {s}: {n}")

# Select 1000
if len(all_q) >= 1000:
    # Take all from small sources, sample from large
    selected = []
    for source in sorted(by_source.keys()):
        src_qs = [q for q in all_q if q["source"] == source]
        if len(src_qs) <= 100:
            selected.extend(src_qs)
        else:
            n_take = max(50, int(1000 * len(src_qs) / len(all_q)))
            selected.extend(random.sample(src_qs, min(n_take, len(src_qs))))
    if len(selected) > 1000:
        selected = random.sample(selected, 1000)
    elif len(selected) < 1000:
        used = set(id(q) for q in selected)
        unused = [q for q in all_q if id(q) not in used]
        selected.extend(random.sample(unused, min(1000 - len(selected), len(unused))))
else:
    selected = all_q

# Assign IDs
for i, q in enumerate(selected):
    q["eval_id"] = f"Q{i+1:04d}"

print(f"\nSelected: {len(selected)}")
final_sources = {}
for q in selected:
    s = q["source"]
    final_sources[s] = final_sources.get(s, 0) + 1
for s, n in sorted(final_sources.items(), key=lambda x: -x[1]):
    print(f"  {s}: {n}")

out = os.path.join(DATA, "eval_1000q_v2.json")
with open(out, "w") as f:
    json.dump(selected, f, indent=1, ensure_ascii=False)
print(f"\nSaved to {out}")
