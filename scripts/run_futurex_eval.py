#!/usr/bin/env python3
"""
FutureX A/B Evaluation - Focus on financial market questions.
Tests whether Abel's causal graph improves market prediction vs base reasoning.
"""

import json
import subprocess
import os

SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Hand-curated financial questions from FutureX-Past
FINANCIAL_QUESTIONS = [
    {
        "id": "FX_AAPL_HIGH",
        "title": "AAPL high on 2026-01-23",
        "question": "What will the high of Apple stock (AAPL) be for the day on 2026-01-23 (in US$)?",
        "ground_truth": 249.41,
        "type": "numeric",
        "ticker": "AAPL",
        "abel_node": "AAPL.price",
    },
    {
        "id": "FX_LI_HIGH",
        "title": "Li Auto high on 2026-01-27",
        "question": "What will be the high for Li Auto (NASDAQ:LI) for the day on 2026-01-27 (in US$)?",
        "ground_truth": 16.85,
        "type": "numeric",
        "ticker": "LI",
        "abel_node": "LI.price",
    },
    {
        "id": "FX_NASDAQ_OPEN",
        "title": "NASDAQ Composite open on 2026-01-27",
        "question": "What will the NASDAQ Composite Index (.IXIC) open be for the day on 2026-01-27?",
        "ground_truth": 23734.75,
        "type": "numeric",
        "ticker": ".IXIC",
        "abel_node": None,  # index, try query
    },
    {
        "id": "FX_SP500_OPEN",
        "title": "S&P 500 open on 2026-01-26",
        "question": "What will be the day's open of the S&P 500 Index on 2026-01-26?",
        "ground_truth": 6923.23,
        "type": "numeric",
        "ticker": "SPX",
        "abel_node": None,
    },
    {
        "id": "FX_DOW_CLOSE",
        "title": "Dow Jones close on 2026-01-22",
        "question": "What will be the day's close for the Dow Jones Industrial Average on 2026-01-22?",
        "ground_truth": 49384.01,
        "type": "numeric",
        "ticker": "DJI",
        "abel_node": None,
    },
    {
        "id": "FX_NVDA_DIR",
        "title": "NVIDIA stock direction Mar 9-16",
        "question": "Will NVIDIA stock be higher on March 16, 2026 than on March 09, 2026?",
        "ground_truth": "No",
        "type": "binary",
        "ticker": "NVDA",
        "abel_node": "NVDA.price",
    },
    {
        "id": "FX_NVDA_TARGET",
        "title": "NVIDIA hits 170 or 200 first",
        "question": "Nvidia hits 170, 200 or neither first by end of January 2026?",
        "ground_truth": "170",  # answer A = hits 170 first
        "type": "choice",
        "ticker": "NVDA",
        "abel_node": "NVDA.price",
    },
    {
        "id": "FX_TSLA_TARGET",
        "title": "Tesla hits $400 or $500 first",
        "question": "Tesla hits $400 or $500 first before end of January 2026?",
        "ground_truth": "400",  # answer A
        "type": "choice",
        "ticker": "TSLA",
        "abel_node": "TSLA.price",
    },
    {
        "id": "FX_BTC_100K",
        "title": "Bitcoin above $100K on Jan 31",
        "question": "Will Bitcoin close above USD $100,000 on 31 January 2026 (UTC)?",
        "ground_truth": "No",
        "type": "binary",
        "ticker": "BTC",
        "abel_node": "BTCUSD.price",
    },
    {
        "id": "FX_BTC_82K",
        "title": "Bitcoin below $82K in January",
        "question": "Bitcoin below $82K in January?",
        "ground_truth": "Yes",
        "type": "binary",
        "ticker": "BTC",
        "abel_node": "BTCUSD.price",
    },
    {
        "id": "FX_STOCKS_MAR13",
        "title": "Stock prices Mar 13 vs Mar 6",
        "question": "Stock prices on March 13: higher than on March 6? (AAPL, NVDA, MSFT, GOOG, AMZN, TSLA)",
        "ground_truth": "Yes",
        "type": "binary",
        "ticker": "multiple",
        "abel_node": "AAPL.price",  # proxy
    },
    {
        "id": "FX_GOLD_JAN",
        "title": "Gold settle price January",
        "question": "What will Gold (GC) settle at in January? Range options from A-J.",
        "ground_truth": "E",  # specific range
        "type": "choice",
        "ticker": "GC",
        "abel_node": None,
    },
    {
        "id": "FX_CRUDE_JAN",
        "title": "Crude oil settle January",
        "question": "What will Crude Oil (CL) settle at in January?",
        "ground_truth": "F",
        "type": "choice",
        "ticker": "CL",
        "abel_node": None,
    },
    {
        "id": "FX_SP500_Q1",
        "title": "Q1 S&P 500 Performance",
        "question": "Q1 S&P 500 Performance - will it be positive or negative?",
        "ground_truth": "A",  # A = negative (down)
        "type": "choice",
        "ticker": "SPX",
        "abel_node": None,
    },
    {
        "id": "FX_CPI_CHINA",
        "title": "China CPI > 0.2% in February",
        "question": "China's monthly consumer inflation (CPI) greater than 0.2% in February?",
        "ground_truth": "Yes",
        "type": "binary",
        "ticker": "CPI_CN",
        "abel_node": None,
    },
    {
        "id": "FX_USDCNY",
        "title": "USD/CNY exchange rate Mar 30",
        "question": "What will be the value in Chinese Yuan of 100 units of US Dollar at the latest exchange rate on 2026-03-30?",
        "ground_truth": 692.23,
        "type": "numeric",
        "ticker": "USDCNY",
        "abel_node": None,
    },
    {
        "id": "FX_INF_CANADA",
        "title": "December Inflation Canada - Annual",
        "question": "December Inflation Canada - Annual. Options: A=2.1%, B=2.3%, C=2.4%, D=2.0%, E=1.8%",
        "ground_truth": "E",
        "type": "choice",
        "ticker": "CPI_CA",
        "abel_node": None,
    },
    {
        "id": "FX_INF_EURO",
        "title": "December Inflation Eurozone - Annual",
        "question": "December Inflation Eurozone - Annual",
        "ground_truth": "C",
        "type": "choice",
        "ticker": "CPI_EU",
        "abel_node": None,
    },
    {
        "id": "FX_PCE",
        "title": "US PCE annual inflation > 2.9%",
        "question": "Will the US PCE annual inflation be greater than 2.9% in January?",
        "ground_truth": "No",
        "type": "binary",
        "ticker": "PCE",
        "abel_node": None,
    },
    {
        "id": "FX_SP500_SWING",
        "title": "S&P 500 Single-Day Swings Q1",
        "question": "S&P 500 Single-Day Gains and Losses (%) in Q1 - which ranges will be hit?",
        "ground_truth": "B,C,D,E,F",  # multiple swings
        "type": "choice",
        "ticker": "SPX",
        "abel_node": None,
    },
]


def abel_probe(verb, params):
    """Run an Abel probe and return parsed result."""
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "verb", verb,
        "--params-json", json.dumps(params)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr
        data = json.loads(output)
        return data
    except Exception as e:
        return {"ok": False, "error": str(e)}


def abel_normalize(ticker):
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "normalize-node", ticker
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout or result.stderr)
        return data
    except:
        return {"ok": False}


def abel_neighbors(node_id, scope="parents", max_n=5):
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "neighbors", node_id,
        "--scope", scope,
        "--max-neighbors", str(max_n)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout or result.stderr)
        return data
    except:
        return {"ok": False}


def run_abel_analysis(q):
    """Run Abel analysis for a single question. Returns dict of findings."""
    findings = {
        "node_found": False,
        "observe": None,
        "neighbors": None,
        "intervention": None,
        "consensus": None,
    }

    node = q.get("abel_node")

    # Try normalize if no preset node
    if not node:
        norm = abel_normalize(q["ticker"])
        if norm.get("ok"):
            node = norm.get("normalized_node_id")
            findings["node_found"] = True

    if not node:
        # Try query search
        search = abel_probe("extensions.abel.query_node", {
            "search": q["title"],
            "search_mode": "hybrid",
            "top_k": 3
        })
        if search.get("ok"):
            items = search.get("result", {}).get("items", [])
            if items:
                seeds = items[0].get("seed_nodes", [])
                if seeds:
                    node = seeds[0]
                    findings["node_found"] = True

    if node:
        findings["node_found"] = True
        findings["node_id"] = node

        # Observe
        obs = abel_probe("extensions.abel.observe_predict_resolved_time", {
            "target_node": node
        })
        if obs.get("ok"):
            findings["observe"] = obs.get("result", {})

        # Neighbors (parents = drivers)
        nbr = abel_neighbors(node, "parents", 5)
        if nbr.get("ok"):
            findings["neighbors"] = nbr.get("result", {})

        # Neighbors (children = downstream)
        ch = abel_neighbors(node, "children", 5)
        if ch.get("ok"):
            findings["children"] = ch.get("result", {})

    return findings


if __name__ == "__main__":
    results = []

    for q in FINANCIAL_QUESTIONS:
        print(f"\n{'='*60}")
        print(f"{q['id']}: {q['title']}")
        print(f"  Type: {q['type']}, GT: {q['ground_truth']}")

        # Run Abel analysis
        abel = run_abel_analysis(q)
        print(f"  Abel node found: {abel['node_found']}")
        if abel.get('node_id'):
            print(f"  Abel node: {abel['node_id']}")
        if abel.get('observe'):
            pred = abel['observe'].get('prediction')
            direction = abel['observe'].get('predicted_direction')
            print(f"  Observe: prediction={pred}, direction={direction}")
        if abel.get('neighbors'):
            nbrs = abel['neighbors'].get('neighbors', [])
            print(f"  Parents: {len(nbrs)} drivers found")
            for n in nbrs[:3]:
                print(f"    - {n.get('display_name', n.get('node_id', '?'))}")

        results.append({
            "id": q["id"],
            "title": q["title"],
            "type": q["type"],
            "ground_truth": q["ground_truth"],
            "ticker": q["ticker"],
            "abel_findings": abel,
        })

    # Save
    out_path = os.path.join(RESULTS_DIR, "futurex_abel_raw.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*60}")
    print("ABEL COVERAGE SUMMARY")
    found = sum(1 for r in results if r["abel_findings"]["node_found"])
    has_obs = sum(1 for r in results if r["abel_findings"].get("observe"))
    has_nbr = sum(1 for r in results if r["abel_findings"].get("neighbors", {}).get("neighbors"))
    print(f"Node found: {found}/{len(results)}")
    print(f"Has observation: {has_obs}/{len(results)}")
    print(f"Has parent drivers: {has_nbr}/{len(results)}")
