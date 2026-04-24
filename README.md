# Abel Skill Advantage Benchmark

Real A/B testing of **Claude Code alone** vs **Claude Code + [causal-abel](https://github.com/Abel-ai-causality/Abel-skills) skill** across **17,424 questions** from the FOMC/ECB/BIS corpus plus 8 additional central banks and MMLU macro/econometrics.

## Results at a Glance

**Original corpus (15,624 FOMC / ECB / BIS questions):**

| | Count | Rate |
|---|---|---|
| Abel wins (Claude wrong → Abel right) | **1,463** | 9.4% |
| Abel loses (Claude right → Abel wrong) | 760 | 4.9% |
| **Net improvement** | **+703** | **+4.5%** |

**New cross-benchmark A/B (1,800 questions, 9 benchmarks × 200 cases):**

| Benchmark | Claude | +Abel | Δ | Flips | Harms |
|---|---:|---:|---:|---:|---:|
| **BoE** | 37.5% | **74.5%** | **+37.0pp** | 90 | 16 |
| **BoJ** | 84.0% | **95.5%** | **+11.5pp** | 24 | 1 |
| SNB | 69.0% | 74.5% | +5.5pp | 19 | 8 |
| Banxico | 68.0% | 70.5% | +2.5pp | 13 | 8 |
| RBA | 66.5% | 67.5% | +1.0pp | 5 | 3 |
| PBoC | 63.0% | 62.5% | −0.5pp | 9 | 10 |
| BoC | 67.0% | 65.5% | −1.5pp | 12 | 15 |
| MMLU (macro + econometrics) | 95.5% | 94.0% | −1.5pp | 2 | 5 |
| RBI | 63.5% | 54.0% | **−9.5pp** | 19 | 38 |
| **New-corpus net** | **67.5%** | **73.1%** | **+5.6pp** | **193** | **104** |

Full cross-benchmark writeup: [CROSS_BENCHMARK_ANALYSIS.md](CROSS_BENCHMARK_ANALYSIS.md).

## What Was Tested

**Original corpus — 15,624 central bank communications across 6 datasets:**

| Dataset | Entries | Source | Task |
|---------|---------|--------|------|
| FinBen FOMC | 496 | TheFinAI/finben-fomc | Hawkish/Dovish/Neutral |
| FinanceMTEB FOMC | 2,281 | FinanceMTEB/FOMC | Hawkish/Dovish/Neutral |
| GTFinTech FOMC | 149 | gtfintechlab/fomc_communication | Hawkish/Dovish/Neutral |
| Moritz ECB | 2,563 | Moritz-Pfeifer/CentralBankCommunication/ECB | Hawkish/Dovish |
| Moritz FED | 6,618 | Moritz-Pfeifer/CentralBankCommunication/FED | Hawkish/Dovish |
| Moritz BIS | 4,047 | Moritz-Pfeifer/CentralBankCommunication/BIS | Hawkish/Dovish |
| **Total (deduplicated)** | **15,624** | | |

**New corpus — 1,800 questions across 9 benchmarks (200 each):**

| Benchmark | Source | Task |
|---|---|---|
| BoE, BoJ, SNB, Banxico, RBA, PBoC, BoC, RBI | gtfintechlab/model_risk_outputs | Hawkish/Dovish/Neutral |
| MMLU (macroeconomics + econometrics) | cais/mmlu | Multiple choice |

## How Each Question Was Tested

Every question went through two conditions:

**Condition A — Claude Code (no Abel):**
- Agent reads the central bank text
- Classifies as hawkish/dovish/neutral using pure economic reasoning
- No Abel API calls, no causal graph

**Condition B — Claude Code + Abel Skill (full 6-step workflow):**
1. **Classify**: Map to macro nodes (federalFunds, inflationRate, GDP, unemploymentRate)
2. **Hypotheses**: Generate including mandatory contrarian
3. **Graph discovery**: Run real `graph.markov_blanket` API calls via `cap_probe.py` against `https://cap.abel.ai/api`
4. **Verify**: Use blanket structure (inflation↔federalFunds↔GDP↔unemployment) to disambiguate
5. **Web grounding**: Where applicable
6. **Synthesize**: Final classification informed by causal structure

**Scoring**: Both answers independently compared to ground truth label.

A question enters this benchmark only if: **Condition A is wrong AND Condition B is correct.**

## Why Abel Helps

Abel's Markov blanket (`inflation↔federalFunds↔GDP↔unemployment`) resolves **causal ambiguity** in central bank text:

| Pattern | Example | Claude says | Abel says | Truth |
|---------|---------|-------------|-----------|-------|
| Mechanism description misread as stance | "Taylor principle of raising rates in response to inflation" | hawkish | **neutral** | neutral |
| Economic strength misread as neutral | "Credit conditions continued to ease, CRE loans growing" | neutral | **hawkish** | hawkish |
| Subtle dovish concern missed | "Commitment to raising inflation to 2 percent" | neutral | **dovish** | dovish |
| Surface sentiment contradicts direction | "Inflation likely to moderate" (from high base) | dovish | **hawkish** | hawkish |
| Dual-channel rate reasoning | "Will 15Y mortgage rate have increased?" (Fed cuts but inflation sticky) | decrease | **increase** | increase |

## Where Abel Helps Most (and Least)

Synthesizing results across the full 17,424-question corpus:

| Data type | Abel advantage | Why |
|-----------|---------------|-----|
| **BoE minutes (3-class)** | **Very strong** (+37pp) | Claude defaults to neutral on data-print language; Abel forces directional mapping |
| **BoJ statements (3-class)** | **Strong** (+12pp) | Subtle relative moves (BoJ is structurally dovish) caught by causal framing |
| **FOMC 3-class** (hawk/dove/neutral) | **Strong** (+8-15pp) | Abel distinguishes neutral mechanism descriptions from directional stances |
| **ECB hawkish** | **Strong** (+12-15pp) | ECB "structural reform" language reads neutral to Claude but is hawkish in ECB context |
| **BIS hawkish** | **Strong** (+15pp) | Similar to ECB — institutional language that implies hawkish stance |
| **SNB (CHF channel)** | **Moderate** (+5pp) | FX transmission chain maps onto Abel's blanket where Claude reads market commentary |
| **Banxico / RBA** | **Mild** (+1-3pp) | Commodity/peso channels partially map onto the blanket |
| **Moritz FED binary** | **Weak** (0 to −1pp) | Without neutral class, Abel's main advantage (mechanism vs stance) disappears |
| **BoC / PBoC** | **Neutral-to-mild harm** (−1 to −2pp) | Fed-shadow bank (BoC) or administered regime (PBoC) — blanket adds no signal |
| **MMLU textbook MCQ** | **Mild harm** (−1.5pp) | Ceiling effect: Claude at 95.5%, Abel adds interpretation noise |
| **RBI** | **Harm** (−9.5pp) | EM demand-side blanket mismatches rupee / capital-flow / supply-side framings |

## Files

```
skill_advantage_benchmark_1000.json  # ← THE BENCHMARK: 1,463 verified Abel-wins cases (FOMC/ECB/BIS)
data/all_flips_final.json            # Same data, raw format
results/cb_batch_*_ab.json           # Complete A/B results for all 33 batches (15,624 questions)
data/all_central_bank_unique.json    # Source data (15,624 deduplicated entries)
data/cb_batch_*.json                 # Input batches (500 questions each)

# New cross-benchmark A/B results
CROSS_BENCHMARK_ANALYSIS.md          # Full writeup of 9 new benchmarks
results/new_ab_{boe,boj,snb,banxico,rba,pboc,boc,rbi}.json  # 200 cases each
results/mmlu_macro_ab.json           # MMLU macro + econometrics
```

## Reproducibility

```bash
# Install Abel skill
npx --yes skills add https://github.com/Abel-ai-causality/Abel-skills/tree/main/skills --skill causal-abel -g -y

# Download central bank datasets
python3 scripts/mass_download.py

# Build deduplicated pool
# (see scripts/build_final_1000.py for entity extraction logic)

# Run A/B test (launches parallel agents, each processing 500 questions)
# Each agent: reads batch → classifies with pure Claude → runs Abel API → reclassifies → scores
# See results/cb_batch_*_ab.json for outputs
```

## Limitations

1. **Abel also causes harms** (Claude right → Abel wrong — 760 in the original corpus, 104 in the new cross-benchmark set). The flips benchmark only contains the wins.
2. **Abel's advantage concentrates on 3-class tasks** (hawk/dove/neutral) and central banks with distinctive non-Fed transmission channels. On binary tasks, Fed-shadow banks, EM administered regimes, and near-ceiling textbook MCQs, the advantage shrinks, disappears, or reverses.
3. **The "base Claude" is an Agent's reasoning**, not a controlled Claude API call. Different Claude instances may produce different base answers.
4. **Predictive rule from cross-benchmark analysis:** Abel helps when Claude's baseline is 35–70% AND the bank has a non-Fed transmission channel AND statements use convention-driven signaling. Abel hurts when Claude is >90% baseline OR the bank is a Fed-follower OR the economy has administered/capital-controlled monetary regimes.

## License

Apache 2.0. Source datasets retain their original licenses.
