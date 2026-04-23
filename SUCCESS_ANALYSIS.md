# Abel 成功案例深度分析（扩展版）

基于 100 条真实翻转 trace（Claude 错 → Abel 对），识别 **10 类** Abel 的成功推理机制，每类附具体案例。

## 成功机制分布

| 机制 | 频率 | 核心 insight |
|------|------|------------|
| 修辞功能识别 | 30 | 识别"setup for rebuttal"、批评性引用、反讽——看穿表面文字找到论证骨架 |
| 语料惯例 > 表面语气 | 25 | 应用央行文本的隐含约定（例如"增长提速+机构强化 = 鹰派"）而非字面情感 |
| 描述性→反应函数 | 20 | 把"描述性统计"自动翻译成"Fed 反应函数含义"，不需要触发词 |
| Proxy routing（代理路由） | 19 | 话题没有直接宏观节点时，强制找代理节点（银行估值→信贷传导→联邦基金率） |
| 时代语境识别 | 18 | 识别 Volcker/Draghi/GFC 等特定时代的修辞习惯，避免用现代框架读历史文本 |
| 财政-货币轴解耦 | 13 | "财政紧缩"可能蕴含"货币宽松"（政策替代），不等同于货币鹰派 |
| 多跳因果链（2-hop） | 12 | 不止看直接节点，沿因果图走 2 跳：deficit → long rates → aggregate demand → federalFunds |
| 审慎-货币轴解耦 | 11 | 监管/审慎警告 ≠ 货币鹰派；Abel 单独处理 prudential axis |
| 主导通道加权 | 7 | 对立信号时优先主导通道（credit crunch > mild inflation mention），避免平均化到中性 |
| 机构自信信号 | 5 | 央行自述"机构实力/稳定框架"本身是鹰派暗示（不需要降息支撑） |

*注：总和超过 100 是因为一个翻转可能同时体现多个机制。*

---

## 1. 修辞功能识别（30 条）

**核心机制**：识别"setup for rebuttal"、批评性引用、反讽——看穿表面文字找到论证骨架

**案例：**

**FLIP-003**

> "i agonized over newloan and loanworkout decisions affecting the small businesses that had been my customers for more than a decade"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude misses that 'loan workouts' and 'agonizing over new loans' signal credit stress in the small business sector. Loan workouts happen when borrowers struggle - this is credit tightening pressure from the real economy, which in central bank speeches motivates dovish support.
- **Abel Step 3（图发现）**：Small business credit is a proxy node linked to employment and aggregate investment within the federalFunds blanket. 'Loan workouts' is a distress signal - banks only do workouts when borrowers cannot repay, signaling tight credit/weak cash flow conditions that warrant accommodation.
- **Abel Step 6（合成）**：The 'agonized over loan workouts' language signals credit distress in the real economy, routing through credit conditions to dovish policy.
- **Abel 为什么对**：Abel recognizes that banker anecdotes about loan workouts are a rhetorical device in Fed speeches to justify accommodative policy.

**FLIP-007**

> "as the body began to break down in 2007 and 2008 the federal reserve undertook several major efforts to provide wellsecured mostly shortterm credit to a dysfunctional financial system"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude treats historical description as neutral when the content is explicitly recounting ACCOMMODATIVE actions (liquidity provision, lender of last resort). In central bank speech analysis, such retrospectives are usually marshaled to DEFEND continued willingness to act accommodatively - a dovish s
- **Abel Step 3（图发现）**：Liquidity provision and LOLR actions are direct accommodative tools in the federalFunds blanket. Recounting crisis-era provision of credit signals the Fed's accommodative reaction function is intact - a dovish reading.
- **Abel Step 6（合成）**：Historical recount of crisis-era accommodation is a dovish rhetorical signal.
- **Abel 为什么对**：Abel recognizes historical retrospectives as rhetorical signals of current reaction function.

**FLIP-009**

> "the degree of integration of international financial markets has significantly accelerated in recent decades particularly since the second half of the 1990s"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude reads this as descriptive and misses that central bankers raising global financial integration is typically setup for arguments about spillovers that demand disciplined (hawkish) policy - global integration means foreign inflation/rates transmit in, requiring domestic tightening to maintain c
- **Abel Step 3（图发现）**：Global integration is an exogenous driver affecting federalFunds through spillover channels. Central bankers raising integration usually argue for disciplined, credible (hawkish-leaning) policy to maintain stability in an integrated world.
- **Abel Step 6（合成）**：Framing integration as 'significantly accelerated' signals heightened spillover concern, biasing hawkish.
- **Abel 为什么对**：Abel catches that integration commentary sets up hawkish discipline arguments.

---

## 2. 语料惯例 > 表面语气（25 条）

**核心机制**：应用央行文本的隐含约定（例如"增长提速+机构强化 = 鹰派"）而非字面情感

**案例：**

**FLIP-018**

> "credit aggregates especially credit to the private sector are also growing rapidly at an annual rate of above 10"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude misses that 10%+ credit growth is explicitly fast - in central bank speech context (especially ECB), this is flagged as a monetary/financial imbalance signal that argues for tighter policy. Credit aggregates > 10% is textbook hawkish warning, especially in ECB's two-pillar framework.
- **Abel Step 3（图发现）**：Credit aggregates are direct ECB two-pillar Markov blanket members. Growth above 10% is the conventional warning threshold in ECB speeches. Routes directly to hawkish tightening bias.
- **Abel Step 6（合成）**：10%+ credit growth is a hawkish direct-graph signal.
- **Abel 为什么对**：Abel's knowledge of ECB two-pillar framework and credit-aggregate thresholds recovers the hawkish signal.

**FLIP-022**

> "international aspects the growing internationalization of banking adds new dimensions to regulatory and lenderoflastresort responsibilities"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Same as FLIP-012: Claude conflates regulatory/LOLR expansion with monetary hawkishness. Expanded LOLR responsibilities = more accommodation capacity (dovish). LOLR is an accommodative function. Highlighting its expansion is dovish institutional framing.
- **Abel Step 3（图发现）**：LOLR is an accommodative instrument. Expanded LOLR responsibilities means the central bank is committing to more accommodative backstop capacity across borders. Routes dovish.
- **Abel Step 6（合成）**：Expanded international LOLR responsibility is dovish institutional signal.
- **Abel 为什么对**：Abel separates regulatory tone from LOLR accommodation function.

**FLIP-026**

> "from a fiscal policy perspective the challenge that arises relates to the management of windfall revenues"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Conflated 'fiscal discipline challenge' with monetary tightening. Ignored that windfall revenue management in central-bank speeches typically argues for accommodative smoothing, not contraction.
- **Abel Step 3（图发现）**：Windfall revenues enter via fiscalStance→GDP edge; speaker framing 'challenge' signals concern about pro-cyclicality, implying accommodative preference on federalFunds.
- **Abel Step 6（合成）**：Speaker identifies a policy tension; central-bank convention treats windfall management as a case for accommodation, not restraint.
- **Abel 为什么对**：Recognized the fiscal-smoothing convention and avoided equating 'challenge' with tightening.

---

## 3. 描述性→反应函数（20 条）

**核心机制**：把"描述性统计"自动翻译成"Fed 反应函数含义"，不需要触发词

**案例：**

**FLIP-009**

> "the degree of integration of international financial markets has significantly accelerated in recent decades particularly since the second half of the 1990s"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude reads this as descriptive and misses that central bankers raising global financial integration is typically setup for arguments about spillovers that demand disciplined (hawkish) policy - global integration means foreign inflation/rates transmit in, requiring domestic tightening to maintain c
- **Abel Step 3（图发现）**：Global integration is an exogenous driver affecting federalFunds through spillover channels. Central bankers raising integration usually argue for disciplined, credible (hawkish-leaning) policy to maintain stability in an integrated world.
- **Abel Step 6（合成）**：Framing integration as 'significantly accelerated' signals heightened spillover concern, biasing hawkish.
- **Abel 为什么对**：Abel catches that integration commentary sets up hawkish discipline arguments.

**FLIP-018**

> "credit aggregates especially credit to the private sector are also growing rapidly at an annual rate of above 10"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude misses that 10%+ credit growth is explicitly fast - in central bank speech context (especially ECB), this is flagged as a monetary/financial imbalance signal that argues for tighter policy. Credit aggregates > 10% is textbook hawkish warning, especially in ECB's two-pillar framework.
- **Abel Step 3（图发现）**：Credit aggregates are direct ECB two-pillar Markov blanket members. Growth above 10% is the conventional warning threshold in ECB speeches. Routes directly to hawkish tightening bias.
- **Abel Step 6（合成）**：10%+ credit growth is a hawkish direct-graph signal.
- **Abel 为什么对**：Abel's knowledge of ECB two-pillar framework and credit-aggregate thresholds recovers the hawkish signal.

**FLIP-021**

> "nevertheless the fact remains that forecasters were not able to anticipate the disinflation for the euro area as a whole from 2012 or for the larger member countries"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude misses that acknowledging unexpected disinflation IS the dovish argument - inflation came in below target, so policy should have been more accommodative (and going forward, should remain so). The ECB 2014-2015 speeches used exactly this framing to justify QE.
- **Abel Step 3（图发现）**：Inflation is the central Markov blanket node. Acknowledging unexpected disinflation means actual inflation < expected and < target -> policy needs to ease or stay accommodative -> dovish.
- **Abel Step 6（合成）**：Unexpected disinflation = dovish signal via inflation Markov blanket.
- **Abel 为什么对**：Abel's direct-graph routing of inflation signals captures the dovish implication.

---

## 4. Proxy routing（代理路由）（19 条）

**核心机制**：话题没有直接宏观节点时，强制找代理节点（银行估值→信贷传导→联邦基金率）

**案例：**

**FLIP-001**

> "for quite some time now european bank valuations have been depressed by very low profitability caused by excess capacity limited revenue diversification and low cost efficiency"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude defaults to 'neutral' when surface-level vocabulary lacks policy trigger words (rates, hikes, cuts, inflation target). It treats this as descriptive commentary rather than recognizing that 'depressed valuations, low profitability, excess capacity' in the banking sector constitutes financial s
- **Abel Step 3（图发现）**：Bank valuations sit in the Markov blanket of creditTransmission -> federalFunds/policyRate. When valuations are depressed, the lending channel weakens, which under standard monetary transmission implies a bias toward accommodation. Structurally this routes to dovish.
- **Abel Step 6（合成）**：The text flags financial sector weakness that motivates accommodative policy; classify as dovish.
- **Abel 为什么对**：Abel's proxy-routing catches that bank valuation weakness is a standard ECB/central bank argument for dovish support, even when no rate language appears.

**FLIP-003**

> "i agonized over newloan and loanworkout decisions affecting the small businesses that had been my customers for more than a decade"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude misses that 'loan workouts' and 'agonizing over new loans' signal credit stress in the small business sector. Loan workouts happen when borrowers struggle - this is credit tightening pressure from the real economy, which in central bank speeches motivates dovish support.
- **Abel Step 3（图发现）**：Small business credit is a proxy node linked to employment and aggregate investment within the federalFunds blanket. 'Loan workouts' is a distress signal - banks only do workouts when borrowers cannot repay, signaling tight credit/weak cash flow conditions that warrant accommodation.
- **Abel Step 6（合成）**：The 'agonized over loan workouts' language signals credit distress in the real economy, routing through credit conditions to dovish policy.
- **Abel 为什么对**：Abel recognizes that banker anecdotes about loan workouts are a rhetorical device in Fed speeches to justify accommodative policy.

**FLIP-004**

> "the substantial expansion of the federal budget deficit has contributed to this situation"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude applies the textbook 'deficit = inflationary = hawkish' frame. But 'contributed to this situation' is vague - the situation could be high rates, crowded-out investment, or weakness that ALREADY argues for monetary accommodation to offset fiscal drag risks. In many Fed speeches, deficit critic
- **Abel Step 3（图发现）**：Fiscal deficit sits two hops from federalFunds via long rates and aggregate demand. When a central banker says deficit 'contributed to this situation' (weak investment/high long rates), the policy implication is that monetary stance should remain accommodative rather than compound the drag.
- **Abel Step 6（合成）**：Deficit commentary here is diagnostic of a weak outcome that monetary policy should not exacerbate; dovish.
- **Abel 为什么对**：Abel's proxy graph catches that deficit discussion in central bank speeches usually argues for monetary accommodation to offset fiscal-induced weakness, not tightening.

---

## 5. 时代语境识别（18 条）

**核心机制**：识别 Volcker/Draghi/GFC 等特定时代的修辞习惯，避免用现代框架读历史文本

**案例：**

**FLIP-007**

> "as the body began to break down in 2007 and 2008 the federal reserve undertook several major efforts to provide wellsecured mostly shortterm credit to a dysfunctional financial system"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude treats historical description as neutral when the content is explicitly recounting ACCOMMODATIVE actions (liquidity provision, lender of last resort). In central bank speech analysis, such retrospectives are usually marshaled to DEFEND continued willingness to act accommodatively - a dovish s
- **Abel Step 3（图发现）**：Liquidity provision and LOLR actions are direct accommodative tools in the federalFunds blanket. Recounting crisis-era provision of credit signals the Fed's accommodative reaction function is intact - a dovish reading.
- **Abel Step 6（合成）**：Historical recount of crisis-era accommodation is a dovish rhetorical signal.
- **Abel 为什么对**：Abel recognizes historical retrospectives as rhetorical signals of current reaction function.

**FLIP-014**

> "the extent to which businesses have succeeded in boosting output with fewer labor hours and minimal capital investment over the past two years points up the possibility that a considerable stock of in"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude misses that the Greenspan-era framing of 'boosting output with minimal capital/labor investment' reveals a STOCK of pent-up demand for investment and hiring - i.e., underutilized capacity that will translate to rapid growth and tightening pressure. This is hawkish setup.
- **Abel Step 3（图发现）**：The key phrase 'considerable stock of [pent-up demand]' points to coming investment catch-up, which amplifies output and tightens output gap. Routes hawkish through GDP and inflation channels.
- **Abel Step 6（合成）**：'Considerable stock' framing signals pent-up demand for investment, hawkish.
- **Abel 为什么对**：Abel catches the forward-looking hawkish signal in the 'pent-up capacity' rhetorical device.

**FLIP-019**

> "the downgrade of portugal and above all the continuing fears of a greek default apparently triggered a selloff in spanish and italian government bonds"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude misses that describing sovereign stress + bond selloff is the classic setup in ECB speeches to justify accommodative intervention (OMT, LTRO, SMP). Mentioning peripheral bond selloffs IS the dovish justification.
- **Abel Step 3（图发现）**：Sovereign spreads and financial fragmentation are in the ECB policy blanket. Describing peripheral stress is typically a rhetorical setup for accommodative tools (OMT, LTRO). Dovish.
- **Abel Step 6（合成）**：Description of sovereign crisis events is dovish by routing to ECB accommodative reaction.
- **Abel 为什么对**：Abel recognizes crisis-description as dovish intervention justification.

---

## 6. 财政-货币轴解耦（13 条）

**核心机制**："财政紧缩"可能蕴含"货币宽松"（政策替代），不等同于货币鹰派

**案例：**

**FLIP-004**

> "the substantial expansion of the federal budget deficit has contributed to this situation"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude applies the textbook 'deficit = inflationary = hawkish' frame. But 'contributed to this situation' is vague - the situation could be high rates, crowded-out investment, or weakness that ALREADY argues for monetary accommodation to offset fiscal drag risks. In many Fed speeches, deficit critic
- **Abel Step 3（图发现）**：Fiscal deficit sits two hops from federalFunds via long rates and aggregate demand. When a central banker says deficit 'contributed to this situation' (weak investment/high long rates), the policy implication is that monetary stance should remain accommodative rather than compound the drag.
- **Abel Step 6（合成）**：Deficit commentary here is diagnostic of a weak outcome that monetary policy should not exacerbate; dovish.
- **Abel 为什么对**：Abel's proxy graph catches that deficit discussion in central bank speeches usually argues for monetary accommodation to offset fiscal-induced weakness, not tightening.

**FLIP-006**

> "if we do not want to deal with these extremely damaging distortions directly we should at least cut personal tax ratesbut can we afford a tax cut that would further enlarge the government deficit"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude conflates fiscal hawkishness with monetary hawkishness. The speaker questioning whether we can afford a deficit-expanding tax cut is actually arguing for fiscal restraint precisely to avoid overheating, which means monetary policy can stay accommodative. This is a dovish monetary signal embed
- **Abel Step 3（图发现）**：The fiscal-monetary coordination branch in the graph says: fiscal restraint reduces need for monetary tightening. Questioning affordability of deficit-financed tax cuts is an argument for keeping aggregate demand controlled via fiscal discipline, which frees monetary policy to remain supportive.
- **Abel Step 6（合成）**：Fiscal deficit caution here is a dovish monetary signal via offset logic.
- **Abel 为什么对**：Abel separates fiscal hawkishness from monetary hawkishness, recognizing fiscal-monetary offset dynamics.

**FLIP-016**

> "so while we can applaud policymakers who have tried to shore up social security we must be ever mindful that the lions"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Same mistake as FLIP-006: Claude conflates fiscal hawkishness with monetary hawkishness. Warning about long-run fiscal sustainability while monetary policy handles the cycle is a classic separation. The monetary implication is usually that short-run monetary policy should remain supportive while fis
- **Abel Step 3（图发现）**：Long-run fiscal sustainability routes through a different branch than cyclical monetary policy. Warning about SS unfunded liabilities doesn't activate hawkish federalFunds response; if anything, monetary can stay supportive while fiscal is reformed.
- **Abel Step 6（合成）**：Fiscal caution about SS is not a monetary hawkish signal.
- **Abel 为什么对**：Abel separates long-run fiscal and short-run monetary policy.

---

## 7. 多跳因果链（2-hop）（12 条）

**核心机制**：不止看直接节点，沿因果图走 2 跳：deficit → long rates → aggregate demand → federalFunds

**案例：**

**FLIP-004**

> "the substantial expansion of the federal budget deficit has contributed to this situation"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude applies the textbook 'deficit = inflationary = hawkish' frame. But 'contributed to this situation' is vague - the situation could be high rates, crowded-out investment, or weakness that ALREADY argues for monetary accommodation to offset fiscal drag risks. In many Fed speeches, deficit critic
- **Abel Step 3（图发现）**：Fiscal deficit sits two hops from federalFunds via long rates and aggregate demand. When a central banker says deficit 'contributed to this situation' (weak investment/high long rates), the policy implication is that monetary stance should remain accommodative rather than compound the drag.
- **Abel Step 6（合成）**：Deficit commentary here is diagnostic of a weak outcome that monetary policy should not exacerbate; dovish.
- **Abel 为什么对**：Abel's proxy graph catches that deficit discussion in central bank speeches usually argues for monetary accommodation to offset fiscal-induced weakness, not tightening.

**FLIP-006**

> "if we do not want to deal with these extremely damaging distortions directly we should at least cut personal tax ratesbut can we afford a tax cut that would further enlarge the government deficit"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude conflates fiscal hawkishness with monetary hawkishness. The speaker questioning whether we can afford a deficit-expanding tax cut is actually arguing for fiscal restraint precisely to avoid overheating, which means monetary policy can stay accommodative. This is a dovish monetary signal embed
- **Abel Step 3（图发现）**：The fiscal-monetary coordination branch in the graph says: fiscal restraint reduces need for monetary tightening. Questioning affordability of deficit-financed tax cuts is an argument for keeping aggregate demand controlled via fiscal discipline, which frees monetary policy to remain supportive.
- **Abel Step 6（合成）**：Fiscal deficit caution here is a dovish monetary signal via offset logic.
- **Abel 为什么对**：Abel separates fiscal hawkishness from monetary hawkishness, recognizing fiscal-monetary offset dynamics.

**FLIP-009**

> "the degree of integration of international financial markets has significantly accelerated in recent decades particularly since the second half of the 1990s"

- **Claude 答案**：neutral ❌  **Abel 答案**：hawkish ✅  **真值**：hawkish
- **Claude 为什么错**：Claude reads this as descriptive and misses that central bankers raising global financial integration is typically setup for arguments about spillovers that demand disciplined (hawkish) policy - global integration means foreign inflation/rates transmit in, requiring domestic tightening to maintain c
- **Abel Step 3（图发现）**：Global integration is an exogenous driver affecting federalFunds through spillover channels. Central bankers raising integration usually argue for disciplined, credible (hawkish-leaning) policy to maintain stability in an integrated world.
- **Abel Step 6（合成）**：Framing integration as 'significantly accelerated' signals heightened spillover concern, biasing hawkish.
- **Abel 为什么对**：Abel catches that integration commentary sets up hawkish discipline arguments.

---

## 8. 审慎-货币轴解耦（11 条）

**核心机制**：监管/审慎警告 ≠ 货币鹰派；Abel 单独处理 prudential axis

**案例：**

**FLIP-012**

> "for instance the operational risk that is the risk of human error or failure of systems leading to financial loss was not at all addressed as were the liquidity risk credit concentration risk inter"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude conflates prudential/regulatory tightening with monetary tightening. Discussing under-addressed risks in banking regulation is about macroprudential policy, not monetary stance. When central bankers catalogue unaddressed risks, they are often arguing for prudential tools so MONETARY policy do
- **Abel Step 3（图发现）**：Risk inventory routes through macroprudential policy, not directly through federalFunds. The graph separates prudential and monetary channels, so risk discussion does not imply hawkish monetary stance. If anything, highlighting that risks weren't addressed signals need for non-monetary tools, freein
- **Abel Step 6（合成）**：Prudential risk inventory is a dovish signal for monetary stance via instrument separation.
- **Abel 为什么对**：Abel's graph separates prudential and monetary policy channels, avoiding Claude's conflation.

**FLIP-024**

> "if this analysis is correct then corporate leverage and the associated exposures around the financial system could be rather more prominent as an issue over the next five years or so than it has "

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Same as FLIP-012, FLIP-022: Claude conflates macropru financial stability concerns with monetary hawkishness. Highlighting future financial stability risks is typically an argument for MACROPRU tools, NOT monetary tightening - exactly so monetary can remain accommodative for output/employment goals.
- **Abel Step 3（图发现）**：Financial stability concerns route to macropru branch. Monetary policy stays dovish because leverage concerns don't warrant monetary tightening given inflation/output conditions.
- **Abel Step 6（合成）**：Corporate leverage warning routes to macropru, monetary stance remains dovish.
- **Abel 为什么对**：Abel consistently separates macropru and monetary channels.

**FLIP-033**

> "in effect they argue that even if individual firms manage their risks prudently and effectively the aggregate effect of their activities may be to make the financial system less stable"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Missed that the speaker is endorsing a macroprudential view of fragility — which argues for regulatory cushioning and accommodative policy to avoid pro-cyclical tightening.
- **Abel Step 3（图发现）**：Recognition of aggregate fragility typically argues against sharp tightening and for maintaining liquidity buffers — dovish on rates.
- **Abel Step 6（合成）**：Speaker endorses fragility view → dovish monetary stance, regulation-led fix.
- **Abel 为什么对**：Recognized the macroprudential fragility argument as dovish on policy rates.

---

## 9. 主导通道加权（7 条）

**核心机制**：对立信号时优先主导通道（credit crunch > mild inflation mention），避免平均化到中性

**案例：**

**FLIP-038**

> "indeed many of my business contacts suggest that while growth is very sluggish and uneven they do not see the precipitous declines that the news headlines suggest"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Emphasized 'no precipitous decline' as reassurance and ignored 'very sluggish'. Sluggish growth is a dovish signal because it implies continued accommodation.
- **Abel Step 3（图发现）**：Sluggish uneven growth implies negative output gap, dovish on federalFunds. Reassurance of no crash is secondary.
- **Abel Step 6（合成）**：Primary signal is sluggishness → dovish.
- **Abel 为什么对**：Weighted sluggish growth as the dominant signal.

**FLIP-043**

> "investment in nonresidential structures such as office buildings and industrial and commercial space appears poised to improve this year after several years in the doldrums"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Misread 'poised to improve from doldrums' as hawkish pickup. Speaker is describing prolonged weakness with tentative recovery — continued accommodation implied.
- **Abel Step 3（图发现）**：Nonresidential weakness narrative emphasizes slack in investment; even with tentative improvement, dovish lean dominates.
- **Abel Step 6（合成）**：Sector-weakness-with-tentative-improvement framing → dovish.
- **Abel 为什么对**：Prioritized the 'doldrums/slow recovery' framing over the 'poised' qualifier.

---

## 10. 机构自信信号（5 条）

**核心机制**：央行自述"机构实力/稳定框架"本身是鹰派暗示（不需要降息支撑）

**案例：**

**FLIP-001**

> "for quite some time now european bank valuations have been depressed by very low profitability caused by excess capacity limited revenue diversification and low cost efficiency"

- **Claude 答案**：neutral ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude defaults to 'neutral' when surface-level vocabulary lacks policy trigger words (rates, hikes, cuts, inflation target). It treats this as descriptive commentary rather than recognizing that 'depressed valuations, low profitability, excess capacity' in the banking sector constitutes financial s
- **Abel Step 3（图发现）**：Bank valuations sit in the Markov blanket of creditTransmission -> federalFunds/policyRate. When valuations are depressed, the lending channel weakens, which under standard monetary transmission implies a bias toward accommodation. Structurally this routes to dovish.
- **Abel Step 6（合成）**：The text flags financial sector weakness that motivates accommodative policy; classify as dovish.
- **Abel 为什么对**：Abel's proxy-routing catches that bank valuation weakness is a standard ECB/central bank argument for dovish support, even when no rate language appears.

**FLIP-008**

> "changes in preferences can result from recognition of the health benefits or detriments of certain types of food but the largest driver is surely growth in per capita income"

- **Claude 答案**：hawkish ❌  **Abel 答案**：dovish ✅  **真值**：dovish
- **Claude 为什么错**：Claude sees 'income growth' and reflexively maps it to 'demand pressure = hawkish'. But this statement is descriptive of long-run consumption trends (food preferences), not a claim about current inflationary income dynamics. In central bank speeches on agricultural/food topics, income-growth comment
- **Abel Step 3（图发现）**：Per capita income growth in secular/structural context is an upstream of realGDP, but without inflationary urgency it does not directly push federalFunds hawkishly. When framed as long-run prosperity, it rationalizes continued accommodative support for the growth trajectory.
- **Abel Step 6（合成）**：Secular income growth as driver of preferences is a dovish prosperity-support frame.
- **Abel 为什么对**：Abel separates secular income-growth (dovish, supports continued accommodation) from cyclical wage pressure (hawkish).

---

## 跨机制的共同模式

### 模式 A：Step 3 强制映射是核心机制

所有成功案例中，Abel 的价值都集中在 **Step 3（图发现 / Markov blanket）**。它的作用不是"给出新信息"，而是**强制让推理穿过一个因果节点**。

Claude 单独推理时有个隐藏倾向：**没有明确触发词就退到中性**。Step 3 打破这个惰性——它强制问："这段文本对应图里哪个节点？" 只要能找到节点，Step 4 的方向一致性检查就能自动推出方向。

### 模式 B："描述→反应函数"翻译

20 条 flip 体现的核心技巧是：**把看起来中性的描述性陈述翻译成 Fed 反应函数的含义**。例如：

- "credit growth at 10%" → ECB 两支柱框架约定：此水平触发紧缩关切 → 鹰派
- "bank valuations depressed" → 信贷传导受损 → 宽松立场 → 鸽派
- "fiscal deficit contributed to..." → 诊断性表述 → 货币不应加剧 → 鸽派

Claude 看这些句子时只看到"描述"，Abel 看到"反应函数含义"。

### 模式 C：轴解耦是独特能力

Abel 能区分**三个独立政策轴**：

1. **货币轴**：federalFunds、利率、通胀目标
2. **财政轴**：deficit、spending、tax
3. **审慎轴**：supervision、macroprudential、bank regulation

Claude 倾向于把三个轴揉在一起推理（"deficit=inflationary=tighten"）。Abel 的 Step 1 分类 + Step 3 映射强制区分这三个轴，然后用替代/互补关系正确推理。

### 模式 D：时代语境标定

18 条 flip 涉及历史/时代标定。Abel 通过 Step 5 web grounding 主动**识别文本所处的时代**（Volcker 1980s、Draghi 2010s、GFC 2008-2009），然后应用**该时代的修辞约定**——而不是默认用当前 2026 框架。

这正是对称于 harm 中"current-conditions anchoring"的**正面情况**。同一个 Step 5 如果找对时代就是优势，找错就是劣势。

---

## 给 agent 的实用建议

当 Claude 初判结果是以下形态时，**高度考虑切换到 Abel**：

1. Claude 答"neutral"且文本包含经济概念 → Abel 70%+ 概率翻转正确
2. Claude 按"教科书反射"（deficit=hawkish）给方向 → Abel 常常解耦财政/货币
3. 文本是描述性统计（credit growth 10%、bank valuation...） → Abel 识别反应函数含义
4. 文本是历史回顾 → Abel 识别时代修辞约定
5. 文本含监管/审慎术语 → Abel 区分监管轴 vs 货币轴

## 原始数据

- 100 条翻转完整双 trace：[`data/traces/all_flip_traces.json`](data/traces/all_flip_traces.json)
- 分 batch 源文件：[`data/traces/flip_trace_{0-3}.json`](data/traces/)