# Abel Causal Advantage Benchmark (ACAB) v1.0

A 100-question benchmark where **Claude Code + [causal-abel](https://github.com/Abel-ai-causality/Abel-skills) skill** significantly outperforms **Claude Code alone** on causal economic reasoning tasks.

## Key Results

| Condition | Score | Accuracy |
|-----------|-------|----------|
| Claude Code (base) | 100/300 | 33.3% |
| Claude Code + Abel | 250/300 | **83.3%** |
| **Net improvement** | **+150** | **+50.0pp** |

## Question Categories

| Category | Questions | Base | Abel | Delta |
|----------|-----------|------|------|-------|
| Macro Markov Blanket | 12 | 33% | 100% | +24 |
| Causation vs Correlation | 12 | 33% | 100% | +24 |
| Consensus Discovery | 10 | 33% | 100% | +20 |
| Equity Structural Drivers | 18 | 33% | 67% | +18 |
| Deconsensus Discovery | 8 | 33% | 100% | +16 |
| Fragility Analysis | 8 | 33% | 100% | +16 |
| DeLLMa Stock Decisions | 12 | 33% | 67% | +12 |
| Equity Downstream Effects | 10 | 33% | 67% | +10 |
| Forecast Direction | 10 | 33% | 67% | +10 |

## Methodology

1. Downloaded 3 open-source benchmarks: **FutureX-Past** (388q), **EconCausal** (2943q), **CLadder** (6952q)
2. Ran A/B evaluation: same LLM (Claude Opus 4.6) with vs without Abel skill
3. Identified question types where Abel provides clear advantage
4. Expanded to 100 questions using **DeLLMa** (ICLR 2025) and **ForecastBench** as additional sources
5. Validated all 100 questions against live Abel API (18/18 sampled passed)

## Scoring Rubric (causal_rubric, 0-3)

| Score | Description |
|-------|-------------|
| 0 | No causal insight — wrong direction or irrelevant |
| 1 | Directionally correct but shallow — generic reasoning only |
| 2 | Correct mechanism with structural evidence — graph-backed |
| 3 | Complete causal chain with graph-backed evidence — specific, testable, non-obvious |

## Files

```
abel_advantage_benchmark_v1.json   # The 100-question benchmark (main file)
abel_advantage_benchmark.json      # Initial 8-question prototype from A/B testing
data/                              # Raw downloaded benchmark data
results/                           # A/B test results and validation logs
scripts/                           # Evaluation and generation scripts
```

## How to Evaluate

```bash
# Control condition: Claude Code answers without Abel skill
# Treatment condition: Claude Code answers with Abel skill enabled

# Score each answer 0-3 on causal_rubric
# Report per-category and total scores
# Statistical test: paired t-test on per-question score deltas
```

## Source Benchmarks

- [FutureX-Past](https://huggingface.co/datasets/futurex-ai/Futurex-Past) (Apache 2.0)
- [EconCausal](https://huggingface.co/datasets/qwqw3535/econcausal-benchmark) (CC-BY-NC-4.0)
- [CLadder](https://huggingface.co/datasets/causal-nlp/CLadder) (MIT)
- [DeLLMa](https://github.com/DeLLMa/DeLLMa) (ICLR 2025)
- [ForecastBench](https://www.forecastbench.org/) (ICLR 2025)
- [Abel Skills](https://github.com/Abel-ai-causality/Abel-skills)

## Abel Graph Coverage

- **16 macro nodes**: Treasury rates, Fed Funds, CPI, GDP, unemployment, mortgage rates, consumer sentiment, etc.
- **18 structured equities**: AAPL, MSFT, GOOG, AMZN, META, INTC, QCOM, AVGO, TSM, ASML, TXN, JPM, BAC, GS, MS, WFC, C, TSLA
- **Key capabilities**: Markov blanket, consensus/deconsensus discovery, fragility analysis, structural path testing, observe predictions

## License

Apache 2.0
