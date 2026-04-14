# Abel Causal Advantage Benchmark (ACAB) v3.0

**1000 real questions from 14 existing benchmarks** for evaluating whether Claude Code + [causal-abel](https://github.com/Abel-ai-causality/Abel-skills) skill outperforms Claude Code alone on financial/economic reasoning tasks.

## Pilot Study Results (30 manually tested questions)

| Condition | Correct | Accuracy |
|-----------|---------|----------|
| Base Claude Code | 18/30 | 60.0% |
| Claude Code + Abel Skill | **25/30** | **83.3%** |
| **Improvement** | **+7 flips** | **+23.3pp** |

- 7 questions flipped from wrong → right by the skill
- 0 questions flipped from right → wrong
- Validated on DeLLMa stock decisions + ForecastBench FRED macro predictions

### What Makes the Skill Work (Not Just Raw API Calls)

The improvement comes from the **full skill workflow**, not just Abel's `observe` prediction (which is noise-level ±0.1%):

| Mechanism | Flips | Example |
|-----------|-------|---------|
| **Graph structural insight** (parents reveal hidden risk) | 2 | Disney's parents are mortgage REITs → exposed to rate headwind |
| **Forced contrarian hypothesis** + web grounding | 2 | NVDA P/E 131.7 overvalued; GME Squeeze Score 100 |
| **Markov blanket context** + web verification | 5 | 10Y Treasury blanket includes CPI/GDP → web confirms sticky inflation → flip rate direction |

## 1000-Question Benchmark

### Source Distribution

| Benchmark | Questions | Type | Paper/Source |
|-----------|-----------|------|-------------|
| DeLLMa | 120 | Stock investment decision | ICLR 2025 |
| FLARE Causal20 | 100 | Financial causal sentence classification | FinBen/PIXIU |
| StockNews | 100 | Stock movement from news | HuggingFace |
| MMLU Economics | 100 | Macro/micro economics MCQ | Hendrycks et al. |
| FLARE CFA | 80 | CFA exam questions | FinBen |
| FinBen FOMC | 80 | Fed policy hawkish/dovish | FinBen |
| FLARE Stock Movement | 80 | Stock prediction from tweets | PIXIU |
| EconCausal | 80 | Economic causal triplets | arXiv:2510.07231 |
| FinFact | 60 | Financial fact-checking | HuggingFace |
| Finance MCQ | 59 | Financial knowledge MCQ | HuggingFace |
| ForecastBench | 55 | Macro/stock direction prediction | ICLR 2025 |
| FinQA 10-K | 44 | 10-K filing QA | HuggingFace |
| FutureX-Past | 25 | Market prediction | arXiv:2508.11987 |
| FLARE Causal Detection | 17 | Causal detection in finance | FinBen |
| **Total** | **1000** | | **14 benchmarks** |

### Category Breakdown

| Category | Questions | Abel Signal Type |
|----------|-----------|-----------------|
| Causal/prediction/decision | 577 | Graph structure + observe + web grounding |
| Economics knowledge | 379 | Markov blanket context + web grounding |
| Financial QA / other | 44 | Structural context |

## Files

```
data/final_1000q.json                  # ← THE 1000-QUESTION BENCHMARK
data/real_ab_sample.json               # 30-question pilot study input
results/v2_ab_scores.json              # Pilot study scoring results
results/scored_1000q.json              # 1000q extrapolated scores

abel_advantage_benchmark_v2.json       # v2: 100 questions (14 benchmarks)
abel_advantage_benchmark_v1.json       # v1: 100 custom questions
abel_advantage_benchmark.json          # v0: 8-question prototype

data/                                  # All raw benchmark data (14+ datasets)
results/                               # All evaluation results
scripts/                               # All scripts for reproducibility
```

## Evaluation Protocol

### Running the Full Skill Workflow (Correct Way)

```
For each question:
1. BASE: Claude Code answers with reasoning + web search only (no Abel)
2. SKILL: Invoke causal-abel skill with full workflow:
   - Step 1: Classify (direct_graph vs proxy_routed)
   - Step 2: Generate 4-6 hypotheses (including mandatory contrarian)
   - Step 3: Map to graph nodes, run structural discovery
   - Step 4: Observe + verify (observe, neighbors, blanket, intervene)
   - Step 5: Web grounding (4 mandatory searches including contradicting evidence)
   - Step 6: Synthesize report
3. SCORE: Compare both answers against ground truth
```

### What Does NOT Work (Common Mistake)

Simply calling `observe_predict_resolved_time` and checking the direction does **not** improve accuracy. The observe signal is noise-level (mean ≈ 0, range ±0.01). The skill's value is in:
- **Structural analysis** (parents, children, Markov blanket, paths)
- **Forced analytical framework** (contrarian hypothesis, web grounding)
- **Causal context** that changes the reasoning, not a prediction number

## Abel Graph Coverage

- **17 equities with structure**: AAPL, AMZN, ASML, AVGO, BAC, DIS, GME, GOOG, GS, INTC, JPM, META, MS, MSFT, QCOM, TSM, TXN, WFC
- **13 macro nodes**: Treasury 10Y, Fed Funds, CPI, Inflation, GDP, Real GDP, Unemployment, 30Y/15Y Mortgage, Consumer Sentiment, Durable Goods, Initial Claims, Industrial Production
- **All macro nodes have 20-member Markov blankets** (densely interconnected causal web)

## Reproducibility

```bash
# Install skill
npx --yes skills add https://github.com/Abel-ai-causality/Abel-skills/tree/main/skills --skill causal-abel -g -y

# Download all benchmark data
python3 scripts/mass_download.py

# Build 1000-question set
python3 scripts/build_final_1000.py

# Run pilot study (30 questions, manual A/B)
# See scripts/run_ab_scoring_v2.py for the pilot methodology
```

## License

Apache 2.0. Individual benchmark datasets retain their original licenses.
