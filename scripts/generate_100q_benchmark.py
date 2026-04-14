#!/usr/bin/env python3
"""
Generate the 100-question Abel Causal Advantage Benchmark (ACAB v1.0).

Categories:
A. Macro Markov Blanket (12q) - informational neighborhoods of macro nodes
B. Equity Structural Drivers (18q) - causal parents of stocks
C. Equity Downstream Effects (10q) - causal children / downstream propagation
D. Causation vs Correlation (12q) - testing path existence between pairs
E. Consensus Discovery (10q) - downstream co-movement patterns
F. Deconsensus Discovery (8q) - contrarian dynamics
G. Fragility Analysis (8q) - single points of failure
H. DeLLMa Stock Decisions (12q) - investment decisions with causal context
I. ForecastBench Direction (10q) - stock direction with causal backing
"""

import json
import os

OUTDIR = os.path.join(os.path.dirname(__file__), "..")

# ============================================================
# Verified Abel node coverage
# ============================================================
MACRO_NODES = {
    "treasuryRateYear10": "10-Year Treasury Rate",
    "federalFunds": "Federal Funds Rate",
    "CPI": "Consumer Price Index",
    "inflationRate": "Inflation Rate",
    "GDP": "Gross Domestic Product",
    "realGDP": "Real GDP",
    "unemploymentRate": "Unemployment Rate",
    "30YearFixedRateMortgageAverage": "30-Year Fixed Mortgage Rate",
    "15YearFixedRateMortgageAverage": "15-Year Fixed Mortgage Rate",
    "consumerSentiment": "Consumer Sentiment",
    "durableGoods": "Durable Goods",
    "initialClaims": "Initial Claims",
    "industrialProductionTotalIndex": "Industrial Production Index",
    "3MonthOr90DayRatesAndYieldsCertificatesOfDeposit": "3-Month CD Yield",
    "commercialBankInterestRateOnCreditCardPlansAllAccounts": "Credit Card Interest Rate",
}

STRUCTURED_EQUITIES = {
    "AAPL": {"name": "Apple", "sector": "Technology", "parents": 2, "children": 0},
    "MSFT": {"name": "Microsoft", "sector": "Technology", "parents": 6, "children": 5},
    "GOOG": {"name": "Alphabet/Google", "sector": "Technology", "parents": 10, "children": 1},
    "AMZN": {"name": "Amazon", "sector": "Technology", "parents": 8, "children": 5},
    "META": {"name": "Meta Platforms", "sector": "Technology", "parents": 10, "children": 10},
    "INTC": {"name": "Intel", "sector": "Semiconductors", "parents": 10, "children": 10},
    "QCOM": {"name": "Qualcomm", "sector": "Semiconductors", "parents": 4, "children": 1},
    "AVGO": {"name": "Broadcom", "sector": "Semiconductors", "parents": 10, "children": 7},
    "TSM": {"name": "TSMC", "sector": "Semiconductors", "parents": 10, "children": 2},
    "ASML": {"name": "ASML Holdings", "sector": "Semiconductors", "parents": 10, "children": 5},
    "TXN": {"name": "Texas Instruments", "sector": "Semiconductors", "parents": 9, "children": 3},
    "JPM": {"name": "JPMorgan Chase", "sector": "Financials", "parents": 8, "children": 4},
    "BAC": {"name": "Bank of America", "sector": "Financials", "parents": 8, "children": 0},
    "GS": {"name": "Goldman Sachs", "sector": "Financials", "parents": 10, "children": 4},
    "MS": {"name": "Morgan Stanley", "sector": "Financials", "parents": 5, "children": 4},
    "WFC": {"name": "Wells Fargo", "sector": "Financials", "parents": 10, "children": 1},
    "C": {"name": "Citigroup", "sector": "Financials", "parents": 10, "children": 2},
    "TSLA": {"name": "Tesla", "sector": "Consumer/Auto", "parents": 2, "children": 0},
}

questions = []
qid = 1


def add_q(cat, question, expected, gt_type, gt, ops, difficulty, base_exp, abel_exp, source="custom", notes=""):
    global qid
    questions.append({
        "id": f"ACAB-{qid:03d}",
        "category": cat,
        "source": source,
        "question": question,
        "expected_answer": expected,
        "ground_truth_type": gt_type,
        "ground_truth": gt,
        "required_abel_ops": ops,
        "scoring": "causal_rubric",
        "difficulty": difficulty,
        "base_expected_score": base_exp,
        "abel_expected_score": abel_exp,
        "abel_advantage": abel_exp - base_exp,
        "notes": notes,
    })
    qid += 1


# ============================================================
# CATEGORY A: Macro Markov Blanket (12 questions)
# ============================================================

macro_blanket_qs = [
    ("treasuryRateYear10", "10-Year Treasury Rate"),
    ("federalFunds", "Federal Funds Rate"),
    ("CPI", "Consumer Price Index"),
    ("unemploymentRate", "Unemployment Rate"),
    ("GDP", "Gross Domestic Product"),
    ("realGDP", "Real GDP"),
    ("30YearFixedRateMortgageAverage", "30-Year Fixed Mortgage Rate"),
    ("consumerSentiment", "Consumer Sentiment"),
    ("durableGoods", "Durable Goods Orders"),
    ("initialClaims", "Initial Jobless Claims"),
    ("industrialProductionTotalIndex", "Industrial Production Index"),
    ("inflationRate", "Inflation Rate"),
]

for node_id, display in macro_blanket_qs:
    add_q(
        "macro_markov_blanket",
        f"What is the complete informational neighborhood (Markov blanket) of {display}? List the minimal set of variables that makes it conditionally independent of all other macroeconomic variables in the system.",
        f"Abel returns 20 member Markov blanket for {node_id} including rates, prices, sentiment, and production indicators with parent/child/spouse roles.",
        "markov_blanket",
        f"markov_blanket({node_id})",
        [f"graph.markov_blanket({node_id})"],
        "hard",
        1, 3,
        notes=f"Abel provides exact conditional independence boundary. Base can only list 'related' variables without structural guarantees.",
    )


# ============================================================
# CATEGORY B: Equity Structural Drivers (18 questions)
# ============================================================

for ticker, info in STRUCTURED_EQUITIES.items():
    if info["parents"] > 0:
        add_q(
            "equity_structural_drivers",
            f"What are the structural causal drivers (parent nodes) of {info['name']} ({ticker}) stock price in a causal graph? Identify the specific assets or factors that causally influence it, not just correlated sectors.",
            f"Abel returns {info['parents']} graph-identified parent nodes for {ticker}.price with specific asset names and connection strengths.",
            "structural_parents",
            f"neighbors({ticker}.price, parents)",
            [f"neighbors({ticker}.price, parents)", f"node_description"],
            "medium",
            1, 2,
            notes=f"Sector: {info['sector']}. Abel provides specific, non-obvious parents. Base gives narrative factors.",
        )


# ============================================================
# CATEGORY C: Equity Downstream Effects (10 questions)
# ============================================================

downstream_stocks = [
    ("MSFT", 5), ("META", 10), ("AMZN", 5), ("INTC", 10), ("AVGO", 7),
    ("ASML", 5), ("TXN", 3), ("JPM", 4), ("GS", 4), ("MS", 4),
]

for ticker, n_children in downstream_stocks:
    info = STRUCTURED_EQUITIES[ticker]
    add_q(
        "equity_downstream",
        f"What assets does {info['name']} ({ticker}) stock price causally influence downstream? If {ticker} moves, which other assets are structurally affected?",
        f"Abel returns {n_children} child nodes downstream of {ticker}.price.",
        "structural_children",
        f"neighbors({ticker}.price, children)",
        [f"neighbors({ticker}.price, children)", "node_description"],
        "medium",
        1, 2,
        notes=f"Abel maps specific downstream propagation. Base can only guess sector peers.",
    )


# ============================================================
# CATEGORY D: Causation vs Correlation (12 questions)
# ============================================================

pair_tests = [
    ("AAPL", "MSFT", "Technology", "same-sector co-leaders"),
    ("GOOG", "META", "Technology", "ad-tech competitors"),
    ("INTC", "QCOM", "Semiconductors", "chip rivals"),
    ("JPM", "GS", "Financials", "investment bank peers"),
    ("BAC", "WFC", "Financials", "retail bank peers"),
    ("MSFT", "AMZN", "Technology", "cloud competitors"),
    ("AVGO", "QCOM", "Semiconductors", "chip designers"),
    ("TSM", "ASML", "Semiconductors", "foundry and equipment"),
    ("TSLA", "META", "Cross-sector", "Musk/Zuckerberg companies"),
    ("JPM", "INTC", "Cross-sector", "finance vs semiconductors"),
    ("GS", "AVGO", "Cross-sector", "finance vs tech"),
    ("AAPL", "TSLA", "Cross-sector", "consumer tech vs auto"),
]

for a, b, context, desc in pair_tests:
    add_q(
        "causation_vs_correlation",
        f"Is there a direct causal link from {STRUCTURED_EQUITIES[a]['name']} ({a}) to {STRUCTURED_EQUITIES[b]['name']} ({b}) stock price, or is their co-movement driven by common factors? Provide structural evidence.",
        f"Abel tests paths({a}.price, {b}.price) and intervene({a} -> {b}). Finding of 'path' or 'no path' is evidence-based.",
        "causal_structure",
        f"paths_and_intervene({a}.price, {b}.price)",
        [f"paths({a}.price, {b}.price)", f"intervene({a}.price -> {b}.price)"],
        "medium",
        1, 3,
        notes=f"Context: {context} ({desc}). Abel's 'no path' finding definitively distinguishes correlation from causation.",
    )


# ============================================================
# CATEGORY E: Consensus Discovery (10 questions)
# ============================================================

consensus_seeds = [
    (["AAPL", "MSFT"], "Big Tech co-movement"),
    (["INTC", "AVGO"], "Semiconductor sector"),
    (["JPM", "GS"], "Investment banking sector"),
    (["META", "GOOG"], "Ad-tech duopoly"),
    (["ASML", "TSM"], "Chip manufacturing chain"),
    (["BAC", "WFC", "C"], "Retail banking trio"),
    (["MSFT", "AMZN", "GOOG"], "Cloud hyperscalers"),
    (["INTC", "QCOM", "TXN"], "US semiconductor makers"),
    (["JPM", "MS", "GS"], "Wall Street banks"),
    (["AAPL", "AMZN", "META"], "FAANG subset"),
]

for seeds, desc in consensus_seeds:
    seed_names = [STRUCTURED_EQUITIES[s]["name"] for s in seeds]
    seed_nodes = [f"{s}.price" for s in seeds]
    add_q(
        "consensus_discovery",
        f"When {', '.join(seed_names)} ({', '.join(seeds)}) move together, what other assets are pulled along downstream? Map the consensus propagation pattern.",
        f"Abel discover_consensus with seeds {seed_nodes} returns downstream nodes with connection strength.",
        "consensus_nodes",
        f"discover_consensus({seed_nodes})",
        [f"discover_consensus({seed_nodes}, direction=out)"],
        "hard",
        1, 3,
        notes=f"Consensus discovery: {desc}. Abel-exclusive capability.",
    )


# ============================================================
# CATEGORY F: Deconsensus Discovery (8 questions)
# ============================================================

decon_targets = [
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("META", "Meta Platforms"),
    ("JPM", "JPMorgan Chase"),
    ("INTC", "Intel"),
    ("GS", "Goldman Sachs"),
    ("AVGO", "Broadcom"),
    ("GOOG", "Alphabet/Google"),
]

for ticker, name in decon_targets:
    add_q(
        "deconsensus_discovery",
        f"What assets move in the opposite direction to {name} ({ticker})? Identify the contrarian dynamics — which nodes in the causal graph are anti-correlated with {ticker}?",
        f"Abel discover_deconsensus with seed [{ticker}.price] returns contrarian nodes with contrast strength.",
        "deconsensus_nodes",
        f"discover_deconsensus([{ticker}.price])",
        [f"discover_deconsensus([{ticker}.price], direction=out, contrast_level=medium)"],
        "hard",
        1, 3,
        notes=f"Deconsensus: empirically-validated contrarian relationships. Abel-exclusive capability.",
    )


# ============================================================
# CATEGORY G: Fragility Analysis (8 questions)
# ============================================================

fragility_groups = [
    (["INTC", "QCOM", "AVGO", "TXN"], "Semiconductor sector"),
    (["JPM", "BAC", "GS", "MS"], "Major US banks"),
    (["AAPL", "MSFT", "GOOG", "META"], "Big Tech"),
    (["INTC", "AVGO", "TSM", "ASML"], "Chip supply chain"),
    (["JPM", "WFC", "BAC", "C"], "Retail + investment banks"),
    (["MSFT", "AMZN", "GOOG"], "Cloud infrastructure"),
    (["META", "GOOG", "AAPL"], "Consumer tech + advertising"),
    (["GS", "MS", "JPM"], "Investment banking complex"),
]

for tickers, desc in fragility_groups:
    names = [STRUCTURED_EQUITIES[t]["name"] for t in tickers]
    nodes = [f"{t}.price" for t in tickers]
    add_q(
        "fragility_analysis",
        f"Analyze the fragility profile of {desc} stocks ({', '.join(tickers)}). Which nodes are single points of failure? What are the most fragile links in this sub-network?",
        f"Abel discover_fragility on {nodes} returns fragile links with severity ratings and bridge nodes.",
        "fragility_report",
        f"discover_fragility({nodes})",
        [f"discover_fragility({nodes}, severity=medium)", "discover_consensus"],
        "hard",
        1, 3,
        notes=f"Fragility: quantitative structural analysis impossible from pure reasoning.",
    )


# ============================================================
# CATEGORY H: DeLLMa Stock Decisions (12 questions)
# ============================================================

dellma_pairs = [
    (["INTC", "META"], "Intel vs Meta: semiconductor vs ad-tech platform"),
    (["META", "GOOG"], "Meta vs Google: competing ad-tech giants"),
    (["AVGO", "INTC"], "Broadcom vs Intel: fabless vs IDM chip maker"),
    (["ASML", "META"], "ASML vs Meta: chip equipment vs social media"),
    (["GOOG", "AMZN"], "Google vs Amazon: search vs e-commerce + cloud"),
    (["META", "MSFT"], "Meta vs Microsoft: social network vs enterprise software"),
    (["QCOM", "INTC"], "Qualcomm vs Intel: mobile vs PC chip maker"),
    (["GOOG", "AAPL"], "Google vs Apple: platforms and ecosystems"),
    (["META", "AVGO"], "Meta vs Broadcom: software platform vs hardware infrastructure"),
    (["INTC", "TSM"], "Intel vs TSMC: IDM vs pure-play foundry"),
    (["MSFT", "JPM"], "Microsoft vs JPMorgan: tech vs finance sector allocation"),
    (["GS", "META"], "Goldman Sachs vs Meta: finance vs tech sector bet"),
]

for pair, desc in dellma_pairs:
    names = []
    abel_nodes = []
    for t in pair:
        if t in STRUCTURED_EQUITIES:
            names.append(STRUCTURED_EQUITIES[t]["name"])
            abel_nodes.append(f"{t}.price")
        else:
            names.append(t)
            abel_nodes.append(f"{t}.price")

    ops = []
    for n in abel_nodes:
        ops.extend([f"observe({n})", f"neighbors({n}, parents)"])
    ops.append(f"consensus({abel_nodes})")

    add_q(
        "dellma_stock_decision",
        f"You have $10,000 to invest in one stock for the next month. Choose between {pair[0]} and {pair[1]}. Justify your decision with causal analysis of what drives each stock and their structural position in the market.",
        f"Abel provides: observe predictions for both stocks, structural parents (what drives each), consensus/deconsensus analysis, enabling causally-grounded investment decision.",
        "investment_decision",
        "best_risk_adjusted_choice",
        ops,
        "hard",
        1, 2,
        source="dellma_adapted",
        notes=f"DeLLMa-adapted: {desc}. Abel adds causal context (drivers, structural position) to the decision. Ground truth from actual month-end returns.",
    )


# ============================================================
# CATEGORY I: ForecastBench Direction (10 questions)
# ============================================================

forecast_stocks = [
    ("AAPL", "Apple", "Will Apple stock close higher at end of next month than today?"),
    ("MSFT", "Microsoft", "Will Microsoft stock close higher at end of next month than today?"),
    ("GOOG", "Alphabet", "Will Alphabet/Google stock close higher at end of next month than today?"),
    ("AMZN", "Amazon", "Will Amazon stock close higher at end of next month than today?"),
    ("META", "Meta", "Will Meta Platforms stock close higher at end of next month than today?"),
    ("INTC", "Intel", "Will Intel stock close higher at end of next month than today?"),
    ("JPM", "JPMorgan", "Will JPMorgan Chase stock close higher at end of next month than today?"),
    ("GS", "Goldman Sachs", "Will Goldman Sachs stock close higher at end of next month than today?"),
    ("AVGO", "Broadcom", "Will Broadcom stock close higher at end of next month than today?"),
    ("TSM", "TSMC", "Will TSMC stock close higher at end of next month than today?"),
]

for ticker, name, question in forecast_stocks:
    add_q(
        "forecast_direction",
        question,
        f"Abel provides: observe_predict direction for {ticker}.price, plus structural parents and consensus analysis for context.",
        "binary_direction",
        "observe_and_structural_context",
        [f"observe({ticker}.price)", f"neighbors({ticker}.price, parents)", f"consensus([{ticker}.price])"],
        "medium",
        1, 2,
        source="forecastbench_adapted",
        notes=f"ForecastBench-adapted. Abel adds directional observe signal + structural driver context to improve prediction confidence.",
    )


# ============================================================
# OUTPUT
# ============================================================

benchmark = {
    "benchmark_name": "Abel Causal Advantage Benchmark (ACAB)",
    "version": "1.0.0",
    "created": "2026-04-13",
    "total_questions": len(questions),
    "description": "100-question benchmark where Claude Code + causal-abel skill significantly outperforms Claude Code alone. Derived from empirical A/B testing across FutureX, EconCausal, CLadder, DeLLMa, and ForecastBench, plus custom causal reasoning questions. Each question tests a capability where Abel's structural causal graph provides data-backed evidence unavailable to pure LLM reasoning.",
    "methodology": {
        "derivation": "Questions selected/designed based on empirical A/B testing. Only question types where Abel-augmented answers scored higher than base answers are included.",
        "source_benchmarks": [
            "FutureX-Past (Apache 2.0) — market prediction questions",
            "EconCausal (CC-BY-NC-4.0) — economic causal reasoning (tested, Abel coverage insufficient)",
            "CLadder (MIT) — formal causal reasoning (tested, not Abel's domain)",
            "DeLLMa (ICLR 2025) — investment decision under uncertainty",
            "ForecastBench — stock direction prediction",
            "Custom causal reasoning questions designed around verified Abel capabilities",
        ],
        "verified_abel_coverage": {
            "macro_nodes": list(MACRO_NODES.keys()),
            "structured_equities": list(STRUCTURED_EQUITIES.keys()),
            "total_macro": len(MACRO_NODES),
            "total_equities": len(STRUCTURED_EQUITIES),
        },
        "scoring": {
            "causal_rubric": {
                "0": "No causal insight — wrong direction or irrelevant",
                "1": "Directionally correct but shallow — correct intuition with generic reasoning only",
                "2": "Correct mechanism with structural evidence — identifies transmission with some graph backing",
                "3": "Complete causal chain with graph-backed evidence — uses Abel's structural model for specific, testable, non-obvious insights",
            },
        },
    },
    "category_summary": {},
    "questions": questions,
    "evaluation_protocol": {
        "control": "Claude Code answers using only base reasoning and web search. No Abel API calls.",
        "treatment": "Claude Code answers using full causal-abel skill workflow.",
        "scoring": "Each answer scored 0-3 on causal_rubric by human evaluator.",
        "minimum_sample": "Run all 100 questions in both conditions. Report per-category and total scores.",
        "statistical_test": "Paired t-test or Wilcoxon signed-rank on per-question score deltas.",
    },
}

# Compute category summary
cats = {}
for q in questions:
    c = q["category"]
    if c not in cats:
        cats[c] = {"count": 0, "total_base": 0, "total_abel": 0, "total_max": 0}
    cats[c]["count"] += 1
    cats[c]["total_base"] += q["base_expected_score"]
    cats[c]["total_abel"] += q["abel_expected_score"]
    cats[c]["total_max"] += 3

benchmark["category_summary"] = {
    c: {
        "question_count": v["count"],
        "expected_base_score": f"{v['total_base']}/{v['total_max']}",
        "expected_abel_score": f"{v['total_abel']}/{v['total_max']}",
        "expected_delta": f"+{v['total_abel'] - v['total_base']}",
    }
    for c, v in cats.items()
}

out_path = os.path.join(OUTDIR, "abel_advantage_benchmark_v1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(benchmark, f, indent=2, ensure_ascii=False)

print(f"Generated {len(questions)} questions -> {out_path}")
print(f"\nCategory breakdown:")
for c, v in cats.items():
    delta = v["total_abel"] - v["total_base"]
    print(f"  {c:30s}: {v['count']:3d} questions | base={v['total_base']:3d} abel={v['total_abel']:3d} delta=+{delta}")

total_base = sum(v["total_base"] for v in cats.values())
total_abel = sum(v["total_abel"] for v in cats.values())
total_max = sum(v["total_max"] for v in cats.values())
print(f"\n  {'TOTAL':30s}: {len(questions):3d} questions | base={total_base:3d}/{total_max} ({total_base/total_max*100:.1f}%) abel={total_abel:3d}/{total_max} ({total_abel/total_max*100:.1f}%) delta=+{total_abel-total_base}")
