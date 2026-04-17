# Abel Skill Success & Failure Deep Analysis

Analysis of **1,356 Abel wins** and **679 Abel losses** from A/B testing 15,624 central bank communications.

---

## Part 1: Why Abel Succeeds (1,356 flips)

### Answer Transition Distribution

| Claude → Abel | Count | % | Pattern |
|---|---|---|---|
| neutral → dovish | 413 | 30.5% | **Abel rescues dovish signals Claude defaults to neutral** |
| hawkish → dovish | 409 | 30.2% | Abel catches dovish concern under hawkish-looking surface |
| neutral → hawkish | 303 | 22.3% | **Abel rescues hawkish signals Claude defaults to neutral** |
| dovish → hawkish | 225 | 16.6% | Abel catches hawkish stance in dovish-looking language |
| ≤ 6 | | | (rare: corrections to neutral) |

### Success Mechanism A: Recovering from Claude's neutral over-defaulting (716 cases)

**Core insight**: Claude Code's default heuristic when text is complex is "neutral / no clear stance". Abel's Markov blanket (`inflation↔federalFunds↔GDP↔unemployment`) forces an explicit mapping to policy direction.

**Example (Claude=neutral, Abel=hawkish, gt=hawkish):**
> "Money growth was damped by a rise in the opportunity cost of holding M2 assets (as typically occurs in periods of policy tightening)."

- **Claude's reasoning**: Technical description of money demand → neutral
- **Abel's reasoning**: "Rising opportunity cost of M2" maps to `federalFunds↑` node. Text explicitly says "periods of policy tightening" → hawkish mechanism
- **Why it works**: The blanket forces Abel to search for direction even in analytical language

### Success Mechanism B: Surface-sentiment vs true stance (207+ cases)

**Core insight**: Positive-sounding economic language ("strong growth", "full employment") implies hawkish stance in central bank context (economy at capacity → needs tightening), but Claude reads it as neutral observation.

**Example (Claude=neutral, Abel=hawkish, gt=hawkish):**
> "At the moment, trend growth near full employment appears to be a reasonable prospect in the year ahead."

- **Claude**: Factual forecast statement → neutral
- **Abel**: "Full employment" → `unemploymentRate` at structural floor → inflation pressure via Phillips curve → hawkish
- **Why it works**: Abel's causal chain `unemployment→inflation→rates` activates when seeing labor tightness

### Success Mechanism C: Subtle dovish concern (413 cases)

**Core insight**: Dovish statements often use analytical/hedged language that Claude reads as neutral, but Abel's blanket catches the implicit worry about below-target inflation or weakening activity.

**Example (Claude=neutral, Abel=dovish, gt=dovish):**
> "And no, we're not—we, we have not at all changed our view, and I haven't changed my view that inflation running above 2 percent, moderately above 2 percent, is a desirable thing."

- **Claude**: Discussion of inflation target → neutral
- **Abel**: "Above 2% is desirable" → implies current inflation is below/at 2% → dovish concern about undershooting
- **Why it works**: Abel's `inflationRate` node position matters, not just mention

### Success Mechanism D: Corrected direction flip (634 cases)

**Core insight**: Claude sometimes picks wrong direction because of misleading keywords; Abel's causal structure re-grounds the direction.

**Example (Claude=hawkish, Abel=dovish, gt=dovish):**
> "Even with the improving labor market, I still hear from businesses that qualified workers are difficult to find..."

- **Claude**: "Improving labor market" → hawkish keyword
- **Abel**: Text is about labor market friction constraining growth → dovish concern about supply side
- **Why it works**: Blanket distinguishes "labor tightness via demand" (hawkish) from "labor shortage via supply friction" (dovish)

### Success Mechanism E: Identifying mechanism descriptions (6 cases)

Rare but high-value: Abel correctly classifies analytical/theoretical statements as neutral where Claude assigns a stance.

**Example (Claude=dovish, Abel=neutral, gt=neutral):**
> "The Phillips curve has become, according to most estimates, quite flat in the sense that movements in unemployment have only a modest impact..."

- **Abel**: Describing empirical weakening of unemployment→inflation link → mechanism description, not policy stance → neutral

---

## Part 2: Why Abel Fails (679 harms)

### Answer Transition Distribution

| Claude → Abel | Count | % | Pattern |
|---|---|---|---|
| dovish → hawkish | 250 | 36.8% | **Abel wrongly flips dovish to hawkish** |
| hawkish → dovish | 220 | 32.4% | **Abel wrongly flips hawkish to dovish** |
| hawkish → neutral | 129 | 19.0% | Abel over-flattens hawkish to neutral |
| dovish → neutral | 67 | 9.9% | Abel over-flattens dovish to neutral |
| ≤ 9 | | | (rare: wrong moves from neutral) |

### Failure Mechanism A: Opposite-stance flipping (470 cases, 69% of all failures)

**Core problem**: Abel's macro context (current inflation rising = hawkish bias) anchors interpretation, causing it to misread text from different regimes.

**Example (Claude=hawkish ✓, Abel=dovish ✗, gt=hawkish):**
> "Japanese export growth has slowed considerably in recent months and some categories have actually registered declines."

- **Claude's correct reading**: Slowing exports in context of Japanese economic strength → policy concern about overshooting → hawkish
- **Abel's error**: "Export growth slowed" → GDP weakness → dovish
- **Why it fails**: Abel's current-conditions anchoring overrides historical context. The statement is from an era where this slowdown was itself a hawkish signal (not dovish weakness).

**Example (Claude=dovish ✓, Abel=hawkish ✗, gt=dovish):**
> "With spending by the federal government expected to slow, activities in these industries may be hampered..."

- **Claude's correct reading**: Fiscal tightening → drag on activity → dovish concern
- **Abel's error**: "Federal government slow spending" → fiscal discipline → hawkish
- **Why it fails**: Abel maps "spending slow" to tightening (hawkish direction) without catching that the speaker is **worried** about the drag.

### Failure Mechanism B: Over-flattening to neutral (196 cases, 29% of failures)

**Core problem**: Abel's "mechanism vs stance" heuristic overshoots — it classifies genuinely hawkish/dovish statements as mechanism descriptions when the text has analytical framing.

**Example (Claude=hawkish ✓, Abel=neutral ✗, gt=hawkish):**
> "These circumstances should help our net export position."

- **Claude's correct reading**: "Help net export position" = favorable conditions → economy strengthening → hawkish
- **Abel's error**: Conditional framing ("should help") → possibility/mechanism → neutral
- **Why it fails**: Abel treats conditional language as theoretical when it's actually a forecast statement with directional implication.

### Failure Mechanism C: Institutional/regulatory confusion (67 cases)

**Core problem**: Abel's Markov blanket doesn't cover institutional/regulatory concepts, so when text mixes policy with regulation, Abel loses the policy signal.

**Example (Claude=hawkish ✓, Abel=neutral ✗, gt=hawkish):**
> "Past deregulation should enable businesses to adapt their organizational structures in response to these new opportunities..."

- **Claude**: "New opportunities" in deregulation context → pro-growth signal → hawkish framing
- **Abel**: Regulatory language → outside macro blanket → neutral
- **Why it fails**: Blanket is limited to macro nodes; doesn't extend to regulatory/institutional reasoning.

### Failure Mechanism D: Dual-mandate confusion (7 cases)

**Core problem**: When text mentions BOTH inflation AND employment concerns, Abel gets confused which mandate to prioritize.

**Example (Claude=dovish ✓, Abel=hawkish ✗, gt=dovish):**
> "At home while growth has been reasonably satisfactory, unemployment and inflation continue at excessive levels."

- **Claude**: High unemployment + high inflation = stagflation → dovish concern (growth problem)
- **Abel's error**: "Inflation excessive" → hawkish node activation
- **Why it fails**: Abel's blanket doesn't weight the unemployment concern enough in stagflation context.

### Failure Mechanism E: Positive economic language confusion (16 cases)

**Core problem**: Abel over-associates positive growth language with hawkish stance, missing dovish concerns about overexpansion/deflation risk.

**Example (Claude=dovish ✓, Abel=hawkish ✗, gt=dovish):**
> "This would lead to another round of price increases, overexpansion and possibly ultimate deflation."

- **Claude**: Chain "overexpansion → deflation" = dovish concern about boom-bust
- **Abel's error**: "Price increases" triggers inflation node → hawkish
- **Why it fails**: Abel stops at the first macro keyword trigger instead of tracing the full causal chain.

---

## Part 3: Summary Comparison

| Dimension | Successes (1,356) | Failures (679) |
|-----------|-------------------|----------------|
| Primary mode | Claude over-defaults to neutral | Abel flips to wrong direction |
| Best for | Subtle signals in analytical language | N/A |
| Worst for | Regulatory/institutional text | Regulatory text, stagflation |
| Key strength | `inflation↔federalFunds↔GDP` blanket force mapping | N/A |
| Key weakness | N/A | Historical context, dual-mandate weighting |

### Net effect

- **Flip-to-harm ratio: 2.0** (for every 2 Abel wins, 1 harm)
- **Net accuracy gain: +4.5%** across 15,624 questions
- **Abel is reliably better on**: FOMC 3-class tasks, ECB hawkish texts, subtle mechanism vs stance
- **Abel is unreliable on**: Binary Moritz_FED (no neutral class), institutional language, historical texts from different macro regimes

---

## Part 4: When to Trust Abel (Decision Rule)

Based on this analysis, Abel's correction should be weighted by:

1. **Text contains mentioned Abel nodes** (inflation, employment, growth, rates) — Abel likely helps
2. **Text is analytical/theoretical** — Abel catches mechanism description (helps)
3. **Text mentions dual mandates (both employment AND inflation concern)** — Abel unreliable (hurts)
4. **Text is about regulation/institutions without macro** — Abel neutral-defaulting (hurts)
5. **Text is from pre-2000 Fed speeches** — Abel's current-conditions anchoring may mislead
6. **Claude's answer is "neutral" and confident** — Abel often rescues (helps)
7. **Claude's answer is "dovish/hawkish" and confident** — Abel sometimes flips wrongly (hurts)

### Practical guideline

> Trust Abel when: Claude defaults to neutral, text has clear Abel nodes, mechanism description.
> Trust Claude when: Text is institutional/regulatory, dual-mandate balancing, historical context.
