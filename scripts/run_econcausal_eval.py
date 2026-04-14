#!/usr/bin/env python3
"""
EconCausal A/B Evaluation:
- Control: Base economic reasoning predictions (pre-filled by analyst)
- Treatment: Abel graph-augmented predictions
"""

import json
import subprocess
import os

SKILL_DIR = "/home/zeyu/.claude/skills/causal-abel"
BASE_URL = "https://cap.abel.ai/api"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def abel_query_node(search_term):
    """Search Abel graph for a concept."""
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "verb", "extensions.abel.query_node",
        "--params-json", json.dumps({
            "search": search_term,
            "search_mode": "hybrid",
            "top_k": 3
        })
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout or result.stderr)
        if data.get("ok"):
            items = data.get("result", {}).get("items", [])
            return items
        return []
    except Exception as e:
        return []


def abel_intervene(treatment_node, outcome_node, treatment_value=0.05, horizon=24):
    """Run Abel intervention analysis."""
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "verb", "extensions.abel.intervene_time_lag",
        "--params-json", json.dumps({
            "treatment_node": treatment_node,
            "treatment_value": treatment_value,
            "outcome_node": outcome_node,
            "horizon_steps": horizon,
            "model": "linear"
        })
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout or result.stderr)
        if data.get("ok"):
            return data.get("result", {})
        return {"error": data.get("message", "unknown error")}
    except Exception as e:
        return {"error": str(e)}


def abel_paths(node_a, node_b):
    """Check if there's a causal path between two nodes."""
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/cap_probe.py",
        "--base-url", BASE_URL,
        "paths", node_a, node_b,
        "--max-paths", "3"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout or result.stderr)
        if data.get("ok"):
            return data.get("result", {})
        return {"error": data.get("message", "unknown error")}
    except Exception as e:
        return {"error": str(e)}


# Questions with treatment/outcome and their potential Abel search terms
ECONCAUSAL_ABEL_MAP = [
    {
        "eval_id": "EC_000",
        "treatment_search": "bank credit lending concentration",
        "outcome_search": "interest rate loan",
        "base_prediction": "+",  # naive: more concentration -> higher rates
        "ground_truth": "-",
    },
    {
        "eval_id": "EC_001",
        "treatment_search": "education early childhood",
        "outcome_search": "college education attainment",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_002",
        "treatment_search": "environmental regulation clean air",
        "outcome_search": "manufacturing shipments industrial output",
        "base_prediction": "-",
        "ground_truth": "-",
    },
    {
        "eval_id": "EC_003",
        "treatment_search": "food aid wheat commodity",
        "outcome_search": "conflict war military",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_004",
        "treatment_search": "job loss unemployment layoff",
        "outcome_search": "labor supply employment spouse",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_005",
        "treatment_search": "industry stock returns sector dispersion",
        "outcome_search": "unemployment rate",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_006",
        "treatment_search": "corporate tax rate",
        "outcome_search": "firm profit welfare shareholder",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_007",
        "treatment_search": "capital gains tax",
        "outcome_search": "stock selling capital gains realizations",
        "base_prediction": "-",
        "ground_truth": "-",
    },
    {
        "eval_id": "EC_008",
        "treatment_search": "bank lending business group conglomerate",
        "outcome_search": "small business lending credit",
        "base_prediction": "-",
        "ground_truth": "-",
    },
    {
        "eval_id": "EC_009",
        "treatment_search": "quarter end reporting financial",
        "outcome_search": "credit risk premium consumer lending",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_010",
        "treatment_search": "broadband internet technology access",
        "outcome_search": "stock market investment fund buying",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_011",
        "treatment_search": "mortgage recourse housing",
        "outcome_search": "job mobility labor geographic",
        "base_prediction": "-",
        "ground_truth": "-",
    },
    {
        "eval_id": "EC_012",
        "treatment_search": "private equity carried interest fee",
        "outcome_search": "fund performance returns",
        "base_prediction": "-",  # naive: higher fees -> lower net returns
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_013",
        "treatment_search": "industry investment growth capex",
        "outcome_search": "executive perks compensation",
        "base_prediction": "+",
        "ground_truth": "+",
    },
    {
        "eval_id": "EC_014",
        "treatment_search": "hedge fund capacity constraint",
        "outcome_search": "fund flow performance sensitivity",
        "base_prediction": "-",
        "ground_truth": "-",
    },
]


def run_evaluation():
    results = []

    for item in ECONCAUSAL_ABEL_MAP:
        print(f"\n{'='*60}")
        print(f"Evaluating {item['eval_id']}: GT={item['ground_truth']}, Base={item['base_prediction']}")

        # Search for treatment node
        print(f"  Searching treatment: {item['treatment_search']}")
        t_nodes = abel_query_node(item['treatment_search'])

        # Search for outcome node
        print(f"  Searching outcome: {item['outcome_search']}")
        o_nodes = abel_query_node(item['outcome_search'])

        abel_treatment_nodes = []
        abel_outcome_nodes = []
        intervention_result = None
        path_result = None
        abel_prediction = None

        if t_nodes:
            abel_treatment_nodes = [n.get('seed_nodes', [n.get('node_id', '')])[0]
                                    if n.get('seed_nodes') else n.get('node_id', '')
                                    for n in t_nodes[:2]]
            print(f"  Treatment nodes found: {abel_treatment_nodes}")

        if o_nodes:
            abel_outcome_nodes = [n.get('seed_nodes', [n.get('node_id', '')])[0]
                                  if n.get('seed_nodes') else n.get('node_id', '')
                                  for n in o_nodes[:2]]
            print(f"  Outcome nodes found: {abel_outcome_nodes}")

        # Try intervention if both found
        if abel_treatment_nodes and abel_outcome_nodes:
            t_node = abel_treatment_nodes[0]
            o_node = abel_outcome_nodes[0]
            print(f"  Running intervention: {t_node} -> {o_node}")

            # Check path first
            path_result = abel_paths(t_node, o_node)
            print(f"  Path result: reachable={path_result.get('reachable', 'N/A')}")

            # Run intervention
            intervention_result = abel_intervene(t_node, o_node)
            effect = intervention_result.get('propagated_effect')
            support = intervention_result.get('effect_support', 'none')
            print(f"  Intervention: effect={effect}, support={support}")

            if effect is not None and effect != 0:
                abel_prediction = "+" if effect > 0 else "-"
            elif support == "no_structural_path":
                abel_prediction = None  # Abel can't help
            else:
                abel_prediction = None

        result = {
            "eval_id": item['eval_id'],
            "ground_truth": item['ground_truth'],
            "base_prediction": item['base_prediction'],
            "base_correct": item['base_prediction'] == item['ground_truth'],
            "abel_treatment_nodes": abel_treatment_nodes,
            "abel_outcome_nodes": abel_outcome_nodes,
            "abel_has_path": path_result.get('reachable', False) if path_result else False,
            "abel_intervention_effect": intervention_result.get('propagated_effect') if intervention_result else None,
            "abel_effect_support": intervention_result.get('effect_support', 'none') if intervention_result else 'no_nodes',
            "abel_prediction": abel_prediction,
            "abel_correct": abel_prediction == item['ground_truth'] if abel_prediction else None,
            "abel_helps": (abel_prediction == item['ground_truth'] and item['base_prediction'] != item['ground_truth'])
                          if abel_prediction else False,
        }
        results.append(result)
        print(f"  -> Base correct: {result['base_correct']}, Abel prediction: {abel_prediction}, Abel correct: {result['abel_correct']}")

    return results


if __name__ == "__main__":
    results = run_evaluation()

    # Save results
    out_path = os.path.join(DATA_DIR, "..", "results", "econcausal_ab.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    base_correct = sum(1 for r in results if r['base_correct'])
    abel_with_signal = [r for r in results if r['abel_prediction'] is not None]
    abel_correct = sum(1 for r in abel_with_signal if r['abel_correct'])
    abel_helps = sum(1 for r in results if r['abel_helps'])

    print(f"Base accuracy: {base_correct}/{len(results)} = {base_correct/len(results)*100:.1f}%")
    print(f"Abel coverage: {len(abel_with_signal)}/{len(results)} questions had graph signal")
    if abel_with_signal:
        print(f"Abel accuracy (where signal exists): {abel_correct}/{len(abel_with_signal)} = {abel_correct/len(abel_with_signal)*100:.1f}%")
    print(f"Abel uniquely helped: {abel_helps} questions")
