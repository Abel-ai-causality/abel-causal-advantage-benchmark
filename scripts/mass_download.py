#!/usr/bin/env python3
"""
Mass download benchmarks. Target: 10,000+ questions across 10+ benchmarks.
Focus on anything economic/financial/causal where Abel might help.
"""
import json, os, traceback
from datasets import load_dataset

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA, exist_ok=True)

def save(name, data):
    path = os.path.join(DATA, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"  -> {len(data)} entries saved to {path}")

def try_load(name, hf_id, split="test", config=None, max_n=5000):
    """Try to load a HuggingFace dataset, return list of dicts."""
    print(f"\n{'='*50}")
    print(f"Downloading: {name} ({hf_id})")
    try:
        kwargs = {"split": split}
        if config:
            kwargs["name"] = config
        ds = load_dataset(hf_id, **kwargs, trust_remote_code=True)
        rows = [dict(row) for row in ds]
        if len(rows) > max_n:
            import random
            random.seed(42)
            rows = random.sample(rows, max_n)
        return rows
    except Exception as e:
        # Try other splits
        for alt_split in ["train", "validation", "test", "dev"]:
            if alt_split == split:
                continue
            try:
                kwargs = {"split": alt_split}
                if config:
                    kwargs["name"] = config
                ds = load_dataset(hf_id, **kwargs, trust_remote_code=True)
                rows = [dict(row) for row in ds]
                if len(rows) > max_n:
                    import random; random.seed(42)
                    rows = random.sample(rows, max_n)
                print(f"  (used split '{alt_split}')")
                return rows
            except:
                continue
        print(f"  FAILED: {e}")
        return []


all_questions = []

# 1. MMLU - economics/business/finance subtasks
for subj in ["high_school_macroeconomics", "high_school_microeconomics",
             "econometrics", "professional_accounting", "business_ethics",
             "management", "marketing"]:
    rows = try_load(f"mmlu_{subj}", "cais/mmlu", split="test", config=subj)
    for r in rows:
        all_questions.append({
            "source": "MMLU", "subset": subj,
            "question": r.get("question", ""),
            "choices": r.get("choices", []),
            "answer": r.get("answer", ""),
        })
    print(f"  {subj}: {len(rows)} questions")

save("mmlu_econ", [q for q in all_questions if q["source"] == "MMLU"])

# 2. TruthfulQA
rows = try_load("truthfulqa", "truthful_qa", split="validation", config="multiple_choice")
tqa = []
for r in rows:
    q_text = r.get("question", "")
    # Keep economics/finance related
    econ_kw = ["invest", "stock", "market", "economy", "inflation", "money", "bank",
               "trade", "tax", "price", "profit", "debt", "recession", "gdp",
               "interest rate", "federal reserve", "gold", "bitcoin", "currency",
               "wealth", "income", "wage", "unemployment", "fiscal", "monetary"]
    if any(kw in q_text.lower() for kw in econ_kw):
        tqa.append({
            "source": "TruthfulQA",
            "question": q_text,
            "choices": r.get("mc1_targets", {}).get("choices", []),
            "labels": r.get("mc1_targets", {}).get("labels", []),
        })
print(f"  TruthfulQA econ-filtered: {len(tqa)}")
save("truthfulqa_econ", tqa)
all_questions.extend(tqa)

# 3. BBH causal_judgement
rows = try_load("bbh_causal", "lukaemon/bbh", config="causal_judgement")
bbh = []
for r in rows:
    bbh.append({
        "source": "BBH_causal_judgement",
        "question": r.get("input", ""),
        "answer": r.get("target", ""),
    })
save("bbh_causal", bbh)
all_questions.extend(bbh)

# 4. COPA (causal reasoning)
rows = try_load("copa", "pkavumba/balanced-copa", split="test")
if not rows:
    rows = try_load("copa", "super_glue", split="validation", config="copa")
copa = []
for r in rows:
    copa.append({
        "source": "COPA",
        "premise": r.get("premise", ""),
        "choice1": r.get("choice1", ""),
        "choice2": r.get("choice2", ""),
        "question": r.get("question", ""),  # "cause" or "effect"
        "answer": r.get("label", ""),
    })
save("copa", copa)
all_questions.extend(copa)

# 5. FinQA (financial QA)
rows = try_load("finqa", "ibm/finqa", split="test")
if not rows:
    rows = try_load("finqa", "ChanceFocus/flare-finqa", split="test")
finqa = []
for r in rows:
    finqa.append({
        "source": "FinQA",
        "question": r.get("question", r.get("input", "")),
        "answer": str(r.get("answer", r.get("output", ""))),
        "context": str(r.get("context", r.get("text", "")))[:200],
    })
save("finqa", finqa)
all_questions.extend(finqa)

# 6. ConvFinQA
rows = try_load("convfinqa", "AdaptLLM/ConvFinQA", split="test")
if not rows:
    rows = try_load("convfinqa", "ChanceFocus/flare-convfinqa", split="test")
convfin = []
for r in rows:
    convfin.append({
        "source": "ConvFinQA",
        "question": r.get("question", r.get("input", "")),
        "answer": str(r.get("answer", r.get("output", ""))),
    })
save("convfinqa", convfin)
all_questions.extend(convfin)

# 7. HeadQA (economics exam questions)
rows = try_load("headqa", "dvilares/head_qa", split="test", config="en")
headqa = []
for r in rows:
    cat = r.get("category", "")
    if "econom" in cat.lower() or "business" in cat.lower():
        headqa.append({
            "source": "HeadQA",
            "question": r.get("qtext", ""),
            "answers": [r.get(f"atext_{i}", "") for i in range(1, 5) if r.get(f"atext_{i}")],
            "correct": r.get("ra", ""),
            "category": cat,
        })
print(f"  HeadQA econ: {len(headqa)}")
save("headqa_econ", headqa)
all_questions.extend(headqa)

# 8. CRASS (counterfactual reasoning)
rows = try_load("crass", "sileod/crass", split="test")
if not rows:
    rows = try_load("crass", "tasksource/crass", split="test")
crass = []
for r in rows:
    crass.append({
        "source": "CRASS",
        "premise": r.get("premise", r.get("sentence1", "")),
        "hypothesis": r.get("hypothesis", r.get("sentence2", "")),
        "label": r.get("label", ""),
    })
save("crass", crass)
all_questions.extend(crass)

# 9. e-CARE (causal reasoning explanation)
rows = try_load("ecare", "12ml/e-CARE", split="test")
if not rows:
    rows = try_load("ecare", "tasksource/ecare", split="validation")
ecare = []
for r in rows:
    ecare.append({
        "source": "eCARE",
        "premise": r.get("premise", ""),
        "hypothesis1": r.get("hypothesis1", r.get("ask-for", "")),
        "hypothesis2": r.get("hypothesis2", ""),
        "answer": r.get("label", r.get("answer", "")),
    })
save("ecare", ecare)
all_questions.extend(ecare)

# 10. FLARE FPB (Financial Phrase Bank sentiment)
rows = try_load("fpb", "ChanceFocus/flare-fpb", split="test")
fpb = []
for r in rows:
    fpb.append({
        "source": "FLARE_FPB",
        "text": r.get("input", r.get("sentence", "")),
        "label": r.get("output", r.get("label", "")),
    })
save("flare_fpb", fpb)
all_questions.extend(fpb)

# 11. FLARE FiQA sentiment
rows = try_load("fiqa", "ChanceFocus/flare-fiqasa", split="test")
fiqa = []
for r in rows:
    fiqa.append({
        "source": "FLARE_FiQA",
        "text": r.get("input", r.get("sentence", "")),
        "label": r.get("output", r.get("label", "")),
    })
save("flare_fiqa", fiqa)
all_questions.extend(fiqa)

# 12. FLARE Headlines
rows = try_load("headlines", "ChanceFocus/flare-headlines", split="test")
headlines = []
for r in rows:
    headlines.append({
        "source": "FLARE_Headlines",
        "text": r.get("input", r.get("text", "")),
        "label": r.get("output", r.get("label", "")),
    })
save("flare_headlines", headlines)
all_questions.extend(headlines)

# 13. CFA exam questions (if available)
rows = try_load("cfa", "ChanceFocus/flare-cfa", split="test")
cfa = []
for r in rows:
    cfa.append({
        "source": "CFA",
        "question": r.get("input", r.get("question", "")),
        "answer": r.get("output", r.get("answer", "")),
    })
save("cfa", cfa)
all_questions.extend(cfa)

# Summary
print(f"\n{'='*50}")
print(f"TOTAL: {len(all_questions)} questions downloaded")
sources = {}
for q in all_questions:
    s = q.get("source", "unknown")
    sources[s] = sources.get(s, 0) + 1
for s, c in sorted(sources.items(), key=lambda x: -x[1]):
    print(f"  {s}: {c}")
