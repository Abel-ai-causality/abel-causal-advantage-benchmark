#!/usr/bin/env python3
"""
Full A/B Test: Claude Code vs Claude Code + Abel Skill
Covers FutureX binary/direction questions + custom causal reasoning questions.

Scoring:
- Binary (Yes/No): exact match = 1, wrong = 0
- Direction: correct direction = 1, wrong = 0
- Causal reasoning: rubric-based 0-3 scale
"""

import json
import subprocess
import os
import sys

SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def abel_call(verb, params):
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "verb", verb,
        "--params-json", json.dumps(params)
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout or r.stderr)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def abel_neighbors(node, scope="parents", max_n=5):
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "neighbors", node, "--scope", scope, "--max-neighbors", str(max_n)
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout or r.stderr)
    except:
        return {"ok": False}


def abel_paths(a, b):
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "paths", a, b, "--max-paths", "3"
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout or r.stderr)
    except:
        return {"ok": False}


def abel_intervene(t_node, o_node, t_val=0.05, horizon=24):
    return abel_call("extensions.abel.intervene_time_lag", {
        "treatment_node": t_node, "treatment_value": t_val,
        "outcome_node": o_node, "horizon_steps": horizon, "model": "linear"
    })


def abel_observe(node):
    return abel_call("extensions.abel.observe_predict_resolved_time", {
        "target_node": node
    })


def abel_consensus(seeds, direction="out", limit=5):
    return abel_call("extensions.abel.discover_consensus", {
        "seed_nodes": seeds, "direction": direction, "limit": limit
    })


def abel_fragility(nodes, severity="medium", limit=5):
    return abel_call("extensions.abel.discover_fragility", {
        "node_ids": nodes, "severity_level": severity,
        "only_fragility": True, "limit": limit
    })


# ============================================================
# TEST SET
# ============================================================

TESTS = [
    # --- CATEGORY 1: FutureX Binary/Direction (7 questions) ---
    {
        "id": "T01",
        "category": "futurex_direction",
        "question": "Will NVIDIA stock be higher on March 16, 2026 than on March 09, 2026?",
        "ground_truth": "No",
        "scoring": "exact_match",
        "abel_nodes": ["NVDA.price"],
        "abel_ops": ["observe", "neighbors", "consensus"],
    },
    {
        "id": "T02",
        "category": "futurex_direction",
        "question": "Will Bitcoin close above USD $100,000 on 31 January 2026?",
        "ground_truth": "No",
        "scoring": "exact_match",
        "abel_nodes": ["BTCUSD.price"],
        "abel_ops": ["observe", "neighbors"],
    },
    {
        "id": "T03",
        "category": "futurex_direction",
        "question": "Bitcoin below $82K in January 2026?",
        "ground_truth": "Yes",
        "scoring": "exact_match",
        "abel_nodes": ["BTCUSD.price"],
        "abel_ops": ["observe", "neighbors", "fragility"],
    },
    {
        "id": "T04",
        "category": "futurex_direction",
        "question": "Will the US PCE annual inflation be greater than 2.9% in January 2026?",
        "ground_truth": "No",
        "scoring": "exact_match",
        "abel_nodes": ["PCE.price"],
        "abel_ops": ["observe", "neighbors"],
    },
    {
        "id": "T05",
        "category": "futurex_direction",
        "question": "Stock prices (AAPL, NVDA, MSFT, GOOG, AMZN, TSLA) on March 13: higher than on March 6, 2026?",
        "ground_truth": "Yes",
        "scoring": "exact_match",
        "abel_nodes": ["AAPL.price", "NVDA.price", "TSLA.price"],
        "abel_ops": ["observe", "consensus"],
    },
    {
        "id": "T06",
        "category": "futurex_direction",
        "question": "China's monthly consumer inflation (CPI) greater than 0.2% in February 2026?",
        "ground_truth": "Yes",
        "scoring": "exact_match",
        "abel_nodes": [],
        "abel_ops": [],
    },
    {
        "id": "T07",
        "category": "futurex_direction",
        "question": "Q1 2026 S&P 500 total return: positive or negative?",
        "ground_truth": "negative",
        "scoring": "exact_match",
        "abel_nodes": ["SPX.price"],
        "abel_ops": ["observe", "neighbors", "fragility"],
    },

    # --- CATEGORY 2: Causal Transmission (6 questions) ---
    {
        "id": "T08",
        "category": "causal_transmission",
        "question": "Does a shock to the 10-year Treasury yield causally propagate to NVIDIA stock price? If so, through what mechanism and with what sign?",
        "ground_truth": "negative_transmission",  # higher yields -> lower growth stocks
        "scoring": "causal_rubric",
        "abel_nodes": ["treasuryRateYear10", "NVDA.price"],
        "abel_ops": ["paths", "intervene"],
    },
    {
        "id": "T09",
        "category": "causal_transmission",
        "question": "What is the causal relationship between crude oil prices and airline stock performance? What is the transmission mechanism?",
        "ground_truth": "negative_transmission",  # higher oil -> higher costs -> lower airline profits
        "scoring": "causal_rubric",
        "abel_nodes": ["CL.price"],
        "abel_ops": ["neighbors", "paths", "intervene"],
        "outcome_search": "airline",
    },
    {
        "id": "T10",
        "category": "causal_transmission",
        "question": "If NVIDIA stock price drops 10%, what happens to AMD stock price? Is there causal transmission or just correlation?",
        "ground_truth": "positive_comovement",  # same sector, but may not have direct causal path
        "scoring": "causal_rubric",
        "abel_nodes": ["NVDA.price", "AMD.price"],
        "abel_ops": ["paths", "intervene"],
    },
    {
        "id": "T11",
        "category": "causal_transmission",
        "question": "What drives Tesla's stock price? List the top causal drivers from the graph.",
        "ground_truth": "structural_drivers",
        "scoring": "causal_rubric",
        "abel_nodes": ["TSLA.price"],
        "abel_ops": ["neighbors", "consensus"],
    },
    {
        "id": "T12",
        "category": "causal_transmission",
        "question": "Is there a causal path from Bitcoin price to Coinbase stock? What is the transmission mechanism?",
        "ground_truth": "positive_transmission",  # BTC up -> more trading -> COIN revenue up
        "scoring": "causal_rubric",
        "abel_nodes": ["BTCUSD.price", "COIN.price"],
        "abel_ops": ["paths", "intervene"],
    },
    {
        "id": "T13",
        "category": "causal_transmission",
        "question": "How does the 10-year Treasury yield affect real estate stocks (e.g., SLG, WELL)? What is the causal direction?",
        "ground_truth": "negative_transmission",  # higher rates -> higher cap rates -> lower REIT values
        "scoring": "causal_rubric",
        "abel_nodes": ["treasuryRateYear10", "SLG.price", "WELL.price"],
        "abel_ops": ["paths", "intervene"],
    },

    # --- CATEGORY 3: Intervention Analysis (5 questions) ---
    {
        "id": "T14",
        "category": "intervention",
        "question": "If the 10-year Treasury rate increases by 50bps, what is the estimated effect on Apple stock price over a 1-month horizon?",
        "ground_truth": "negative_effect",
        "scoring": "causal_rubric",
        "abel_nodes": ["treasuryRateYear10", "AAPL.price"],
        "abel_ops": ["intervene"],
        "intervene_params": {"treatment_value": 0.005, "horizon_steps": 170},
    },
    {
        "id": "T15",
        "category": "intervention",
        "question": "If Bitcoin drops 20%, what is the propagated effect on Ethereum price? What is the time lag?",
        "ground_truth": "negative_effect",  # BTC drop -> ETH drops (positive comovement = neg effect from neg shock)
        "scoring": "causal_rubric",
        "abel_nodes": ["BTCUSD.price", "ETHUSD.price"],
        "abel_ops": ["intervene"],
        "intervene_params": {"treatment_value": -0.20, "horizon_steps": 42},
    },
    {
        "id": "T16",
        "category": "intervention",
        "question": "If crude oil prices spike 15%, what downstream effects propagate to transportation and industrial stocks?",
        "ground_truth": "negative_downstream",
        "scoring": "causal_rubric",
        "abel_nodes": ["CL.price"],
        "abel_ops": ["neighbors", "intervene"],
        "intervene_params": {"treatment_value": 0.15, "horizon_steps": 42},
    },
    {
        "id": "T17",
        "category": "intervention",
        "question": "What is the fragility profile of semiconductor stocks? Which nodes are single points of failure?",
        "ground_truth": "fragility_analysis",
        "scoring": "causal_rubric",
        "abel_nodes": ["NVDA.price", "AMD.price", "INTC.price", "QCOM.price"],
        "abel_ops": ["fragility", "consensus"],
    },
    {
        "id": "T18",
        "category": "intervention",
        "question": "If we intervene to increase the unemployment rate, what is the predicted effect on consumer discretionary stocks?",
        "ground_truth": "negative_effect",
        "scoring": "causal_rubric",
        "abel_nodes": ["unemploymentRate"],
        "abel_ops": ["neighbors", "intervene"],
    },

    # --- CATEGORY 4: Structural Discovery (4 questions) ---
    {
        "id": "T19",
        "category": "structural_discovery",
        "question": "What are the consensus downstream effects of a simultaneous move in NVIDIA and AMD? Which sectors get pulled along?",
        "ground_truth": "consensus_sectors",
        "scoring": "causal_rubric",
        "abel_nodes": ["NVDA.price", "AMD.price"],
        "abel_ops": ["consensus"],
    },
    {
        "id": "T20",
        "category": "structural_discovery",
        "question": "What are the contrarian dynamics around Bitcoin? What nodes move OPPOSITE to BTC?",
        "ground_truth": "deconsensus_nodes",
        "scoring": "causal_rubric",
        "abel_nodes": ["BTCUSD.price"],
        "abel_ops": ["deconsensus"],
    },
    {
        "id": "T21",
        "category": "structural_discovery",
        "question": "Map the Markov blanket of the 10-year Treasury rate. What is its complete informational neighborhood?",
        "ground_truth": "markov_blanket",
        "scoring": "causal_rubric",
        "abel_nodes": ["treasuryRateYear10"],
        "abel_ops": ["markov_blanket", "neighbors"],
    },
    {
        "id": "T22",
        "category": "structural_discovery",
        "question": "Find the causal path from the unemployment rate to tech stock prices. How many hops? What are the intermediate nodes?",
        "ground_truth": "causal_path",
        "scoring": "causal_rubric",
        "abel_nodes": ["unemploymentRate", "NVDA.price"],
        "abel_ops": ["paths"],
    },
]


def run_abel_for_question(q):
    """Execute all Abel operations for a question and return findings."""
    findings = {"ops_results": {}}

    for op in q.get("abel_ops", []):
        nodes = q["abel_nodes"]
        if not nodes:
            continue

        if op == "observe":
            for n in nodes:
                key = f"observe_{n}"
                findings["ops_results"][key] = abel_observe(n)

        elif op == "neighbors":
            for n in nodes:
                key = f"neighbors_{n}"
                findings["ops_results"][key] = abel_neighbors(n, "parents", 5)

        elif op == "consensus":
            key = "consensus"
            findings["ops_results"][key] = abel_consensus(nodes[:2])

        elif op == "deconsensus":
            key = "deconsensus"
            findings["ops_results"][key] = abel_call(
                "extensions.abel.discover_deconsensus",
                {"seed_nodes": nodes[:1], "direction": "out",
                 "contrast_level": "medium", "limit": 8}
            )

        elif op == "fragility":
            key = "fragility"
            findings["ops_results"][key] = abel_fragility(nodes[:4])

        elif op == "paths":
            if len(nodes) >= 2:
                key = f"paths_{nodes[0]}_{nodes[1]}"
                findings["ops_results"][key] = abel_paths(nodes[0], nodes[1])

        elif op == "intervene":
            if len(nodes) >= 2:
                params = q.get("intervene_params", {})
                key = f"intervene_{nodes[0]}_{nodes[1]}"
                findings["ops_results"][key] = abel_intervene(
                    nodes[0], nodes[1],
                    params.get("treatment_value", 0.05),
                    params.get("horizon_steps", 24)
                )

        elif op == "markov_blanket":
            cmd = [
                "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
                "--base-url", BASE_URL,
                "verb", "graph.markov_blanket",
                "--params-json", json.dumps({"node_id": nodes[0]})
            ]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                findings["ops_results"]["markov_blanket"] = json.loads(r.stdout or r.stderr)
            except:
                findings["ops_results"]["markov_blanket"] = {"ok": False}

    # Summarize what we got
    findings["has_signal"] = any(
        v.get("ok", False) for v in findings["ops_results"].values()
        if isinstance(v, dict)
    )
    return findings


def summarize_abel_result(op_name, result):
    """One-line summary of an Abel operation result."""
    if not isinstance(result, dict):
        return "error"
    if not result.get("ok", False):
        err = result.get("message", result.get("error", "failed"))
        return f"FAIL: {str(err)[:80]}"

    r = result.get("result", {})
    if "prediction" in r:
        return f"prediction={r['prediction']}, resolved={r.get('resolved_direction','?')}"
    if "neighbors" in r:
        nbrs = r["neighbors"]
        names = [n.get("display_name", n.get("node_id", "?"))[:30] for n in nbrs[:3]]
        return f"{len(nbrs)} neighbors: {names}"
    if "reachable" in r:
        return f"reachable={r['reachable']}, paths={r.get('path_count',0)}"
    if "propagated_effect" in r:
        return f"effect={r['propagated_effect']}, support={r.get('effect_support','?')}"
    if "effect_support" in r:
        return f"support={r['effect_support']}, reachable={r.get('reachable','?')}"
    if "consensus_nodes" in r:
        nodes = r["consensus_nodes"]
        return f"{len(nodes)} consensus nodes"
    if "deconsensus_nodes" in r:
        nodes = r["deconsensus_nodes"]
        return f"{len(nodes)} deconsensus nodes"
    if "fragile_links" in r:
        links = r["fragile_links"]
        return f"{len(links)} fragile links"
    # fallback
    keys = list(r.keys())[:5]
    return f"keys={keys}"


if __name__ == "__main__":
    all_results = []

    for q in TESTS:
        print(f"\n{'='*70}")
        print(f"[{q['id']}] {q['category']}: {q['question'][:80]}")
        print(f"  GT: {q['ground_truth']}")

        findings = run_abel_for_question(q)
        print(f"  Abel has signal: {findings['has_signal']}")

        for op_name, op_result in findings["ops_results"].items():
            summary = summarize_abel_result(op_name, op_result)
            print(f"    {op_name}: {summary}")

        all_results.append({
            "id": q["id"],
            "category": q["category"],
            "question": q["question"],
            "ground_truth": q["ground_truth"],
            "scoring": q["scoring"],
            "abel_nodes": q["abel_nodes"],
            "abel_findings": findings,
        })

    # Save raw results
    out_path = os.path.join(RESULTS_DIR, "full_ab_raw.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n\nRaw results saved to {out_path}")

    # Coverage summary by category
    print(f"\n{'='*70}")
    print("COVERAGE SUMMARY BY CATEGORY")
    print(f"{'='*70}")
    cats = {}
    for r in all_results:
        cat = r["category"]
        if cat not in cats:
            cats[cat] = {"total": 0, "has_signal": 0, "details": []}
        cats[cat]["total"] += 1
        if r["abel_findings"]["has_signal"]:
            cats[cat]["has_signal"] += 1
        cats[cat]["details"].append(f"{r['id']}: signal={r['abel_findings']['has_signal']}")

    for cat, info in cats.items():
        print(f"\n{cat}: {info['has_signal']}/{info['total']} with Abel signal")
        for d in info["details"]:
            print(f"  {d}")
