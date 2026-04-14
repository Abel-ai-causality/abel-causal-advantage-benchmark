#!/usr/bin/env python3
"""
Explore Abel graph coverage: find nodes with rich structure.
Tests a wide range of tickers/macro nodes for neighbors, markov blankets, etc.
"""

import json
import subprocess
import os
import sys

SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"

def probe(args, timeout=20):
    cmd = ["python3", f"{SKILL_DIR}/scripts/cap_probe.py", "--base-url", BASE_URL] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout or r.stderr)
    except:
        return {"ok": False}

def check_node(node_id):
    """Check a node's structural richness."""
    info = {"node_id": node_id, "exists": False, "parents": 0, "children": 0, "observe": False}

    # Parents
    r = probe(["neighbors", node_id, "--scope", "parents", "--max-neighbors", "10"])
    if r.get("ok"):
        info["exists"] = True
        nbrs = r.get("result", {}).get("neighbors", [])
        info["parents"] = len(nbrs)
        info["parent_names"] = [n.get("display_name", n.get("node_id",""))[:40] for n in nbrs[:5]]

    # Children
    r = probe(["neighbors", node_id, "--scope", "children", "--max-neighbors", "10"])
    if r.get("ok"):
        info["exists"] = True
        nbrs = r.get("result", {}).get("neighbors", [])
        info["children"] = len(nbrs)
        info["child_names"] = [n.get("display_name", n.get("node_id",""))[:40] for n in nbrs[:5]]

    # Observe
    r = probe(["verb", "extensions.abel.observe_predict_resolved_time",
               "--params-json", json.dumps({"target_node": node_id})])
    if r.get("ok"):
        info["observe"] = True
        info["prediction"] = r.get("result", {}).get("prediction")

    return info

def check_macro_markov(node_id):
    """Check Markov blanket for macro nodes."""
    r = probe(["verb", "graph.markov_blanket", "--params-json", json.dumps({"node_id": node_id})])
    if r.get("ok"):
        res = r.get("result", {})
        nbrs = res.get("neighbors", [])
        return {
            "node_id": node_id,
            "blanket_size": len(nbrs),
            "blanket_names": [n.get("display_name", n.get("node_id",""))[:40] for n in nbrs[:8]],
        }
    return {"node_id": node_id, "blanket_size": 0}

def search_nodes(query):
    """Search for nodes by keyword."""
    r = probe(["verb", "extensions.abel.query_node",
               "--params-json", json.dumps({"search": query, "search_mode": "hybrid", "top_k": 5})])
    if r.get("ok"):
        items = r.get("result", {}).get("items", [])
        return [{"name": i.get("asset_name", i.get("display_name", "")),
                 "node_id": i.get("seed_nodes", [i.get("node_id")])[0] if i.get("seed_nodes") else i.get("node_id",""),
                 "domain": i.get("domain", ""),
                 "sector": i.get("sector", "")}
                for i in items]
    return []


# ============================================================
# PHASE 1: Test major US equities across sectors
# ============================================================
EQUITIES = [
    # Tech/Semis
    "AAPL.price", "MSFT.price", "GOOG.price", "AMZN.price", "META.price",
    "NVDA.price", "AMD.price", "INTC.price", "QCOM.price", "AVGO.price",
    "TSM.price", "ASML.price", "MU.price", "TXN.price",
    # Finance
    "JPM.price", "BAC.price", "GS.price", "MS.price", "WFC.price", "C.price",
    "BLK.price", "SCHW.price",
    # Healthcare
    "JNJ.price", "UNH.price", "PFE.price", "ABBV.price", "LLY.price", "MRK.price",
    # Energy
    "XOM.price", "CVX.price", "COP.price", "SLB.price",
    "CL.price",  # crude oil futures
    # Consumer
    "WMT.price", "COST.price", "HD.price", "MCD.price", "NKE.price", "SBUX.price",
    # Industrial
    "BA.price", "CAT.price", "GE.price", "HON.price", "UPS.price",
    # Real Estate
    "SLG.price", "WELL.price", "AMT.price", "PLD.price",
    # Crypto
    "BTCUSD.price", "ETHUSD.price", "SOLUSD.price", "XRPUSD.price", "DOGEUSD.price",
    # Others
    "TSLA.price", "DIS.price", "NFLX.price", "COIN.price", "V.price", "MA.price",
]

# Macro nodes to test Markov blankets
MACRO_NODES = [
    "treasuryRateYear10",
    "mortgageRate30Year",
    "mortgageRate15Year",
    "federalFundsRate",
    "unemploymentRate",
    "consumerPriceIndex",
    "m2MoneySupply",
    "retailSales",
    "industrialProduction",
    "housingStarts",
]


if __name__ == "__main__":
    results = {"equities": [], "macro": [], "crypto_pairs": []}

    # Test equities
    print("=== TESTING EQUITIES ===")
    for node in EQUITIES:
        info = check_node(node)
        results["equities"].append(info)
        status = "HAS_STRUCTURE" if info["parents"] > 0 or info["children"] > 0 else ("EXISTS" if info["exists"] else "MISSING")
        obs = "OBS" if info["observe"] else "no-obs"
        print(f"  {node:20s} | {status:14s} | P={info['parents']:2d} C={info['children']:2d} | {obs}")
        if info.get("parent_names"):
            print(f"    parents: {info['parent_names'][:3]}")
        if info.get("child_names"):
            print(f"    children: {info['child_names'][:3]}")

    # Test macro Markov blankets
    print("\n=== TESTING MACRO MARKOV BLANKETS ===")
    for node in MACRO_NODES:
        mb = check_macro_markov(node)
        results["macro"].append(mb)
        print(f"  {node:30s} | blanket={mb['blanket_size']:2d}")
        if mb.get("blanket_names"):
            print(f"    members: {mb['blanket_names'][:5]}")

    # Test some cross-node paths
    print("\n=== TESTING CROSS-NODE PATHS ===")
    path_tests = [
        ("AAPL.price", "MSFT.price"), ("XOM.price", "BA.price"),
        ("JPM.price", "GS.price"), ("TSLA.price", "NKE.price"),
        ("CL.price", "XOM.price"), ("BTCUSD.price", "ETHUSD.price"),
        ("GS.price", "BLK.price"), ("NVDA.price", "TSM.price"),
        ("META.price", "GOOG.price"), ("WMT.price", "COST.price"),
    ]
    path_results = []
    for a, b in path_tests:
        r = probe(["paths", a, b, "--max-paths", "3"])
        reachable = r.get("result", {}).get("reachable", False) if r.get("ok") else "error"
        paths_found = r.get("result", {}).get("path_count", 0) if r.get("ok") else 0
        path_results.append({"from": a, "to": b, "reachable": reachable, "paths": paths_found})
        print(f"  {a:20s} -> {b:20s} | reachable={reachable} paths={paths_found}")

    # Test interventions on pairs with paths
    print("\n=== TESTING INTERVENTIONS ===")
    intervene_tests = [
        ("AAPL.price", "MSFT.price", 0.05, 24),
        ("XOM.price", "COP.price", 0.10, 24),
        ("JPM.price", "BAC.price", -0.05, 24),
        ("CL.price", "BA.price", 0.15, 42),
        ("NVDA.price", "MU.price", -0.10, 24),
        ("BTCUSD.price", "COIN.price", 0.20, 24),
    ]
    intervene_results = []
    for t, o, val, h in intervene_tests:
        r = probe(["verb", "extensions.abel.intervene_time_lag",
                    "--params-json", json.dumps({
                        "treatment_node": t, "treatment_value": val,
                        "outcome_node": o, "horizon_steps": h, "model": "linear"
                    })])
        effect = r.get("result", {}).get("propagated_effect") if r.get("ok") else None
        support = r.get("result", {}).get("effect_support", "error") if r.get("ok") else "error"
        reachable = r.get("result", {}).get("reachable", False) if r.get("ok") else False
        intervene_results.append({
            "treatment": t, "outcome": o, "value": val,
            "effect": effect, "support": support, "reachable": reachable
        })
        print(f"  {t:16s} ({val:+.2f}) -> {o:16s} | effect={effect} support={support}")

    # Save all
    out_path = os.path.join(os.path.dirname(__file__), "..", "results", "graph_exploration.json")
    with open(out_path, "w") as f:
        json.dump({"equities": results["equities"], "macro": results["macro"],
                    "paths": path_results, "interventions": intervene_results}, f, indent=2)
    print(f"\nSaved to {out_path}")

    # Summary
    print("\n=== SUMMARY ===")
    has_struct = sum(1 for e in results["equities"] if e["parents"] > 0 or e["children"] > 0)
    has_obs = sum(1 for e in results["equities"] if e["observe"])
    total = len(results["equities"])
    print(f"Equities: {has_struct}/{total} with structure, {has_obs}/{total} with observe")
    has_mb = sum(1 for m in results["macro"] if m["blanket_size"] > 0)
    print(f"Macro blankets: {has_mb}/{len(results['macro'])} found")
    has_path = sum(1 for p in path_results if p["reachable"])
    print(f"Cross-node paths: {has_path}/{len(path_results)} reachable")
    has_effect = sum(1 for i in intervene_results if i["effect"] is not None)
    print(f"Interventions with effect: {has_effect}/{len(intervene_results)}")
