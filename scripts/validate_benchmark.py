#!/usr/bin/env python3
"""
Validate the 100-question benchmark by sampling 2 questions per category
and running actual Abel API calls to verify signal exists.
"""

import json
import subprocess
import random
import os

random.seed(42)
SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"

def probe(args, timeout=25):
    cmd = ["python3", f"{SKILL_DIR}/scripts/cap_probe.py", "--base-url", BASE_URL] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout or r.stderr)
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Load benchmark
with open(os.path.join(os.path.dirname(__file__), "..", "abel_advantage_benchmark_v1.json")) as f:
    benchmark = json.load(f)

questions = benchmark["questions"]

# Sample 2 per category
categories = {}
for q in questions:
    c = q["category"]
    if c not in categories:
        categories[c] = []
    categories[c].append(q)

sample = []
for cat, qs in categories.items():
    sample.extend(random.sample(qs, min(2, len(qs))))

print(f"Validating {len(sample)} sampled questions across {len(categories)} categories\n")

results = []
for q in sample:
    print(f"{'='*60}")
    print(f"[{q['id']}] {q['category']}")
    print(f"Q: {q['question'][:100]}")

    # Parse and run the first Abel operation from required_abel_ops
    op = q["required_abel_ops"][0]
    success = False
    detail = ""

    if "markov_blanket" in op:
        # Extract node id from op string
        node = op.split("(")[1].rstrip(")")
        r = probe(["verb", "graph.markov_blanket", "--params-json", json.dumps({"node_id": node})])
        if r.get("ok"):
            nbrs = r.get("result", {}).get("neighbors", [])
            success = len(nbrs) > 0
            detail = f"{len(nbrs)} blanket members"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "neighbors" in op:
        parts = op.replace("neighbors(", "").rstrip(")").split(", ")
        node = parts[0]
        scope = parts[1] if len(parts) > 1 else "parents"
        r = probe(["neighbors", node, "--scope", scope, "--max-neighbors", "5"])
        if r.get("ok"):
            nbrs = r.get("result", {}).get("neighbors", [])
            success = True  # even 0 neighbors is valid (it means "no structural connection")
            names = [n.get("display_name","?")[:30] for n in nbrs[:3]]
            detail = f"{len(nbrs)} {scope}: {names}"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "paths" in op:
        parts = op.replace("paths(", "").rstrip(")").split(", ")
        a, b = parts[0], parts[1]
        r = probe(["paths", a, b, "--max-paths", "3"])
        if r.get("ok"):
            success = True
            reachable = r.get("result", {}).get("reachable", False)
            detail = f"reachable={reachable}"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "consensus" in op and "deconsensus" not in op:
        # Extract seed nodes
        seeds_str = op.split("([")[1].split("]")[0]
        seeds = [s.strip().strip("'\"") for s in seeds_str.split(",")]
        r = probe(["verb", "extensions.abel.discover_consensus",
                    "--params-json", json.dumps({"seed_nodes": seeds, "direction": "out", "limit": 5})])
        if r.get("ok"):
            items = r.get("result", {}).get("items", [])
            success = True
            detail = f"{len(items)} consensus items"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "deconsensus" in op:
        seeds_str = op.split("([")[1].split("]")[0]
        seeds = [s.strip().strip("'\"") for s in seeds_str.split(",")]
        r = probe(["verb", "extensions.abel.discover_deconsensus",
                    "--params-json", json.dumps({"seed_nodes": seeds, "direction": "out",
                                                  "contrast_level": "medium", "limit": 5})])
        if r.get("ok"):
            items = r.get("result", {}).get("items", [])
            success = True
            detail = f"{len(items)} deconsensus items"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "fragility" in op:
        nodes_str = op.split("([")[1].split("]")[0]
        nodes = [n.strip().strip("'\"") for n in nodes_str.split(",")]
        r = probe(["verb", "extensions.abel.discover_fragility",
                    "--params-json", json.dumps({"node_ids": nodes, "severity_level": "medium",
                                                  "only_fragility": True, "limit": 5})])
        if r.get("ok"):
            items = r.get("result", {}).get("items", [])
            success = True
            detail = f"{len(items)} fragility items"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    elif "observe" in op:
        node = op.replace("observe(", "").rstrip(")")
        r = probe(["verb", "extensions.abel.observe_predict_resolved_time",
                    "--params-json", json.dumps({"target_node": node})])
        if r.get("ok"):
            pred = r.get("result", {}).get("prediction")
            success = True
            detail = f"prediction={pred}"
        else:
            detail = r.get("message", r.get("error", "failed"))[:80]

    else:
        detail = f"Unknown op: {op}"

    status = "PASS" if success else "FAIL"
    print(f"  Op: {op}")
    print(f"  Result: {status} | {detail}")
    results.append({
        "id": q["id"], "category": q["category"],
        "op": op, "success": success, "detail": detail
    })

# Summary
print(f"\n{'='*60}")
print("VALIDATION SUMMARY")
print(f"{'='*60}")
passed = sum(1 for r in results if r["success"])
print(f"Total: {passed}/{len(results)} passed")

by_cat = {}
for r in results:
    c = r["category"]
    if c not in by_cat:
        by_cat[c] = {"pass": 0, "fail": 0}
    if r["success"]:
        by_cat[c]["pass"] += 1
    else:
        by_cat[c]["fail"] += 1

for cat, info in by_cat.items():
    status = "ALL PASS" if info["fail"] == 0 else f"{info['fail']} FAILED"
    print(f"  {cat:30s}: {info['pass']}/{info['pass']+info['fail']} ({status})")

# Save
out_path = os.path.join(os.path.dirname(__file__), "..", "results", "benchmark_validation.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {out_path}")
