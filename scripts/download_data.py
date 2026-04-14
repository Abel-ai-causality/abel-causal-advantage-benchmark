#!/usr/bin/env python3
"""Download and prepare benchmark datasets for Abel skill evaluation."""

import json
import os
import csv

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def download_futurex_past():
    """Download FutureX-Past dataset (388 resolved prediction questions)."""
    from datasets import load_dataset
    ds = load_dataset("futurex-ai/Futurex-Past", split="train")
    out = []
    for row in ds:
        out.append({
            "id": row["id"],
            "prompt": row["prompt"],
            "title": row["title"],
            "ground_truth": row["ground_truth"],
            "level": row["level"],
            "end_time": row.get("end_time", ""),
            "source": "futurex_past",
        })
    path = os.path.join(DATA_DIR, "futurex_past.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"FutureX-Past: {len(out)} questions -> {path}")
    return out


def download_econcausal():
    """Download EconCausal benchmark tasks."""
    from datasets import load_dataset
    results = []
    for config in ["task1_econ", "task1_finance", "task2", "task3"]:
        try:
            ds = load_dataset("qwqw3535/econcausal-benchmark", config, split="train")
            for row in ds:
                entry = dict(row)
                entry["source"] = f"econcausal_{config}"
                results.append(entry)
        except Exception as e:
            print(f"  Warning: could not load {config}: {e}")
    path = os.path.join(DATA_DIR, "econcausal.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"EconCausal: {len(results)} entries -> {path}")
    return results


def download_cladder():
    """Download CLadder causal reasoning dataset (rung 2-3 only)."""
    from datasets import load_dataset
    ds = load_dataset("causal-nlp/CLadder", split="full_v1.5_default")
    out = []
    for row in ds:
        # Only keep rung 2 (intervention) and rung 3 (counterfactual)
        rung = row.get("rung", 0)
        if rung in [2, 3]:
            out.append({
                "id": row.get("id", ""),
                "prompt": row.get("prompt", ""),
                "label": row.get("label", ""),
                "reasoning": row.get("reasoning", ""),
                "rung": rung,
                "query_type": row.get("query_type", ""),
                "graph_id": row.get("graph_id", ""),
                "source": "cladder",
            })
    path = os.path.join(DATA_DIR, "cladder_rung23.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"CLadder (rung 2-3): {len(out)} questions -> {path}")
    return out


if __name__ == "__main__":
    print("=== Downloading benchmark datasets ===\n")
    download_futurex_past()
    print()
    download_econcausal()
    print()
    download_cladder()
    print("\n=== Done ===")
