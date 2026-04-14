#!/usr/bin/env python3
"""Sample and prepare evaluation questions from benchmarks."""

import json
import random
import os

random.seed(42)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def sample_futurex():
    """Sample 15 econ/finance questions from FutureX-Past."""
    with open(os.path.join(DATA_DIR, "futurex_past.json")) as f:
        fx = json.load(f)

    econ_kw = [
        'stock', 'market', 'GDP', 'inflation', 'interest rate', 'Fed',
        'economy', 'price', 'trade', 'tariff', 'oil', 'gold', 'bitcoin',
        'crypto', '股', '经济', '市场', '通胀', '利率', '关税', '贸易',
        '金融', 'S&P', 'Nasdaq', 'recession', 'growth', 'unemployment',
        'bond', 'yield', 'dollar', 'bank', 'fiscal', 'monetary',
        'currency', 'exchange rate', 'crude', 'commodity', 'housing',
        'CPI', 'PPI', 'PMI', 'treasury', 'revenue', 'earnings',
    ]
    econ_qs = [q for q in fx if any(
        kw.lower() in (q['prompt'] + q['title']).lower() for kw in econ_kw
    )]
    # Prefer higher-difficulty questions (level 3-4)
    hard = [q for q in econ_qs if q['level'] >= 3]
    easy = [q for q in econ_qs if q['level'] < 3]
    sample = random.sample(hard, min(10, len(hard)))
    if len(sample) < 15:
        sample += random.sample(easy, min(15 - len(sample), len(easy)))
    return sample[:15]


def sample_econcausal():
    """Sample 15 causal sign prediction questions from EconCausal."""
    with open(os.path.join(DATA_DIR, "econcausal.json")) as f:
        ec = json.load(f)

    # Only keep entries with clear signs and from task1 (sign prediction)
    task1 = [e for e in ec if e['source'] in ('econcausal_task1_econ', 'econcausal_task1_finance')
             and e.get('answer') in ('+', '-', 'None')]
    # Mix econ and finance
    econ = [e for e in task1 if e['source'] == 'econcausal_task1_econ']
    fin = [e for e in task1 if e['source'] == 'econcausal_task1_finance']
    sample = random.sample(econ, min(8, len(econ))) + random.sample(fin, min(7, len(fin)))
    return sample[:15]


def sample_cladder():
    """Sample 10 intervention/counterfactual questions from CLadder."""
    with open(os.path.join(DATA_DIR, "cladder_rung23.json")) as f:
        cl = json.load(f)

    # Mix rung 2 and rung 3, diverse query types
    rung2 = [q for q in cl if q['rung'] == 2]
    rung3 = [q for q in cl if q['rung'] == 3]
    sample = random.sample(rung2, min(5, len(rung2))) + random.sample(rung3, min(5, len(rung3)))
    return sample[:10]


def format_eval_question(q, idx, benchmark):
    """Format a question for the evaluation set."""
    if benchmark == "futurex":
        return {
            "eval_id": f"FX_{idx:03d}",
            "benchmark": "futurex_past",
            "question": q['prompt'],
            "title": q['title'],
            "ground_truth": q['ground_truth'],
            "difficulty": q['level'],
            "control_answer": None,
            "treatment_answer": None,
            "control_score": None,
            "treatment_score": None,
        }
    elif benchmark == "econcausal":
        return {
            "eval_id": f"EC_{idx:03d}",
            "benchmark": "econcausal",
            "question": q.get('question', ''),
            "treatment_var": q.get('treatment', ''),
            "outcome_var": q.get('outcome', ''),
            "context": q.get('context', ''),
            "ground_truth": q.get('answer', ''),
            "paper_title": q.get('title', ''),
            "control_answer": None,
            "treatment_answer": None,
            "control_score": None,
            "treatment_score": None,
        }
    elif benchmark == "cladder":
        return {
            "eval_id": f"CL_{idx:03d}",
            "benchmark": "cladder",
            "question": q['prompt'],
            "ground_truth": q['label'],
            "rung": q['rung'],
            "query_type": q['query_type'],
            "reasoning": q.get('reasoning', ''),
            "control_answer": None,
            "treatment_answer": None,
            "control_score": None,
            "treatment_score": None,
        }


if __name__ == "__main__":
    eval_set = []

    fx_sample = sample_futurex()
    print(f"FutureX sampled: {len(fx_sample)}")
    for i, q in enumerate(fx_sample):
        eval_set.append(format_eval_question(q, i, "futurex"))

    ec_sample = sample_econcausal()
    print(f"EconCausal sampled: {len(ec_sample)}")
    for i, q in enumerate(ec_sample):
        eval_set.append(format_eval_question(q, i, "econcausal"))

    cl_sample = sample_cladder()
    print(f"CLadder sampled: {len(cl_sample)}")
    for i, q in enumerate(cl_sample):
        eval_set.append(format_eval_question(q, i, "cladder"))

    out_path = os.path.join(DATA_DIR, "eval_set.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(eval_set, f, ensure_ascii=False, indent=2)
    print(f"\nTotal eval set: {len(eval_set)} questions -> {out_path}")

    # Print summary
    for q in eval_set:
        gt = str(q['ground_truth'])[:50]
        qtext = q.get('title', q['question'][:60])
        print(f"  {q['eval_id']} | {qtext[:60]} | GT: {gt}")
