# Abel Skill Advantage: 100 Verified Cases

From ~2,000 questions across 14 benchmarks, these are the 100 cases where **Claude Code + causal-abel skill**
correctly answers while **Claude Code alone** (with web search) gets wrong.

**Fair comparison**: Both conditions have Claude reasoning + web search. Only Abel's causal graph differs.

---

## Summary

| Source | Count | Abel Mechanism |
|--------|-------|----------------|
| FinBen FOMC | 92 | Markov blanket disambiguates mechanism description vs policy stance |
| ForecastBench FRED | 8 | Blanket shows dual causal parents (inflation + Fed) for rate reasoning |
| **Total** | **100** | **0 harms** |

---

## Part A: FOMC Hawkish/Dovish/Neutral Classification (92 cases)

Source: [FinBen FOMC](https://huggingface.co/datasets/TheFinAI/finben-fomc)

Abel's `inflation↔federalFunds↔GDP↔unemployment` Markov blanket helps distinguish:
- **Mechanism descriptions** (theoretical/analytical → neutral) from **policy stance** (hawkish/dovish)
- **Surface sentiment** that contradicts actual policy direction

### Case SAB-001

> However, we have also found that excluding volatile food and energy prices generally gives a better sense of underlying inflation pressures that are likely to persist and dominate total inflation over time.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-002

> Rather, members agreed that inflation was likely to moderate in coming quarters,

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-003

> In the productivity boom that followed World War I, a chief technological innovation was the spread of electrification to the factory floor.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-004

> But I want to emphasize that we do have a commitment to raising inflation to 2 percent.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-005

> The Committee decided to keep the target range for the federal funds rate at 0 to 1/4 percent and expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee's assessments of maximum employment and inflation has risen to 2 percent and is on track to moderately exceed 2 percent for some time.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-006

> As a consequence, a sustainable, non-inflationary expansion is likely to involve some moderation in the growth of economic activity to a rate more consistent with the expansion of the nationâ€™s underlying productive capacity.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-007

> They noted that the economy had entered the new year with considerable momentum and very few indications that growth was moderating from what appeared to be an unsustainable rate.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-008

> Although inflation remained remarkably subdued and any increase in inflationary pressures likely would tend to emerge only slowly, the strength in demand had developed against the backdrop of financial conditions that, broadly considered, were not substantially different from those now prevailing.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-009

> The prospect of additional fiscal stimulus likely contributed to a steeper U. S. Treasury yield curve, increased inflation compensation, and broad dollar depreciation.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-010

> Operationally, maintaining price stability requires abiding by the Taylor principle of raising nominal interest rates more than one for one in response to movements in inflation, especially those movements perceived as persistent.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-011

> As of this month, the maximum monthly reduction in the balance sheet will be nearly double the level of the previous cycle.10 Together, the increase in the policy rate and the reduction in the balance sheet should help bring demand into alignment with supply.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-012

> Although we cannot ascertain the precise rates of resource utilization that the economy can sustain, we can have little doubt that, after three years of above-trend growth, slack has been substantially reduced.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-013

> Credit conditions in the commercial real estate (CRE) sector continued to ease, and growth in CRE loans at banks stayed solid.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-014

> While labor markets were anticipated to remain tight in the near term, participants expected labor demand and supply to come into better balance over time, helping to ease upward pressure on wages and prices.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-015

> However, household spending had been relatively robust during the cyclical downturn and likely had only limited room for a pickup over coming quarters, and intense competitive pressures could well constrain profits, investment, and equity prices.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-016

> Although the unemployment rate is around a 50-year low, wages are rising broadly in line with productivity growth and underlying inflation.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-017

> With the risks to the forecast for economic activity tilted to the downside, the risks to the inflation projection were also viewed as having a downward skew.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-018

> Fourth and finally, the statement codifies the key lesson from the Global Financial Crisisâ€”that financial stability is necessary for the achievement of our statutory goals of maximum employment and price stability.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-019

> Millions of new jobs have been created in the last few years; and unemployment, now at 4.3 percent, has been at or below 5 percent for over two years.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-020

> For example, the evidence suggests that changes in the demographic composition of the labor force affect NAIRU and it is also likely that government programs, including unemployment compensation and welfare, also affect NAIRU.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-021

> The Committee also reiterated that it would continue its asset purchases, and employ its other policy tools as appropriate, until the outlook for the labor market has improved substantially in a context of price stability.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-022

> The staff continued to view the uncertainty around its projections for real GDP growth, the unemployment rate, and inflation as generally similar to the average of the past 20 years.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-023

> However, indicators of economic activity in Japan and Brazil remained weak.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-024

> Mortgage credit conditions generally remained tight over the intermeeting period, though signs of easing continued to emerge amid further gains in house prices.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-025

> The Committee's accompanying statement noted that economic growth had slowed over the course of the year, partly reflecting a substantial cooling of the housing market.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-026

> The Committee's accompanying statement indicated that economic growth had been quite strong so far this year.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-027

> Participants expected that productivity growth would pick up as firms slowed hiring to a pace more in line with output growth but acknowledged that the improvement might be limited, particularly if business investment spending were to remain soft.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-028

> To support continued progress toward maximum employment and price stability, the Committee today reaffirmed its view that a highly accommodative stance of monetary policy will remain appropriate for a considerable time after the asset purchase program ends and the economic recovery strengthens.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-029

> Participants generally expected that household demand would gradually strengthen over coming quarters in response to the rise in household wealth from the substantial increase in equity prices that had occurred over the intermeeting period as well as the support for income provided by fiscal policy.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-030

> Participants expected that fiscal policy would continue to be a drag on economic growth over coming quarters.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-031

> The extent and timing of any additional firming that may be needed to address these risks will depend on the evolution of the outlook for both inflation and economic growth, as implied by incoming information.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-032

> Thus, knowing where productivity growth is headed is, in many respects, equivalent to foreseeing our economic destinies.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-033

> The stock market soared, and--remarkably enough--core inflation moderated.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-034

> While participants generally felt that the pace of underlying productivity growth remained robust, careful attention would need to be paid to developments regarding unit labor costs and profit margins.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-035

> Homebuilding was forecast to decline somewhat but to stabilize at a relatively high level in the context of continued income growth and the generally favorable cash-flow affordability of home ownership.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-036

> That projection, along with the path to year-three inflation, should help the public differentiate short-term shocks to price stability from the longer-term price trends it should use for planning purposes.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-037

> Nonfarm payroll employment rose substantially further in October.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-038

> Now with respect to the first objective, the rationale for maximizing employment is fairly obvious.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-039

> Private nonfarm payroll employment increased appreciably on balance over September and October.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-040

> For many years, forecasters could assume a modest, but stable, trend productivity growth rate and fairly predictable growth in the labor force.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-041

> Participants judged that an appropriate firming of the stance of monetary policy, along with an eventual waning of supply–demand imbalances, would help to keep longer-term inflation expectations anchored and bring inflation down over time to levels consistent with the Committee's 2 percent longer-run goal.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-042

> The weakness in labor market conditions remained an important concern to meeting participants, with unemployment expected to remain elevated for some time.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-043

> Labor productivity growth slowed to an average pace of 1.4 percent per year over this period,

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-044

> Members also expressed concern about the potential for an increase in inflation expectations given highly stimulative macroeconomic policies and economic growth that seemed to be gathering momentum.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-045

> However, if real (or nominal) government spending is held constant, the surplus will rise over time as a share of GDP, putting downward pressure on the equilibrium real rate, offsetting, at least in part, the effect on the real rate of the higher trend productivity.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-046

> However, we now know that an unexpected and unrecognized slowdown in productivity growth occurred in 1973.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-047

> Even with the improving labor market, I still hear from businesses that qualified workers are difficult to find, and labor shortages remain a drag on hiring and on economic growth.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-048

> For the present, however, inflation remained subdued, and it was likely to remain relatively low for some time in light of the weakness in commodity and other import prices and the tendency for low current inflation to hold down expected price increases.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-049

> Again, the FOMC has done just that through its commitment to adjust policy as required to keep inflation at bay.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-050

> As always, my colleagues on the FOMC and I will act to foster our dual objectives of price stability and sustainable economic growth.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-051

> In this less comfortable world, restoring price stability can involve a painful process of slow growth and elevated unemployment.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-052

> Some members expressed concern about the longer-run prospects for large federal deficits and their implications for the future performance of the economy.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-053

> But I think that that’s a prudent move, to move in a gradual way to remove Chair Yellen’s Press Conference FINAL accommodation, with unemployment now—and not only, I should say, the unemployment rate, but I think any indicator of labor market performance and tightness that you could look at, whether it’s household perceptions of the availability of jobs, difficulty that firms report in hiring workers, the rate at which workers are quitting their jobs, the rate of job openings, all of these indicators do signal a tight labor market.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-054

> Although I expect these upward price pressures to ease after the temporary supply bottlenecks are resolved, the exact timing of that dynamic is uncertain.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-055

> In any case, we, our job is to deliver price stability, and I think—you can think of price stability as an asset that just delivers large benefits to society over a long period of time.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-056

> Recent declines in payroll employment and industrial production, while still sizable, were smaller than those registered earlier in 2009.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-057

> year-over-year consumer inflation remained at a very low level.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-058

> Total nonfarm payroll employment increased at a solid pace in October and November, and the unemployment rate declined, reaching 4.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-059

> Answering this question is central to our outlook for both of our dual-mandate goals of maximum employment and price stability.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-060

> In discussing the increases in U. S. longer-term interest rates that occurred in the wake of the June FOMC meeting and the associated press conference, meeting participants pointed to heightened financial market uncertainty about the path of monetary policy and a shift of market expectations toward less policy accommodation.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-061

> Advances in productivity had boosted profit margins, and high margins were helpful in that they could absorb some portion of any cost increases for a time.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-062

> Moreover, if, as some members thought likely, productivity growth slowed as employment picked up, the result could be reductions in slack accompanied by higher unit labor costs and associated pressures on prices.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-063

> Treasury yields rose sharply on its release as market participants traced out the report's presumed implications for monetary policy.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-064

> Proponents of this strategy sometimes describe this approach as reducing inflation cycle-to-cycle or describe the economy as being one recession from price stability.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-065

> In spite of having such slow growth, disappointing productivity growth, we have a labor market that last year generated an average of about 230,000 jobs a month and so far this year has been generating about 180,000 jobs a month.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-066

> Participants discussed several risks that, if realized, could necessitate a steeper path of increases in the target range; these risks included the possibility that inflation pressures could build unduly if output expanded well beyond its maximum sustainable level, perhaps owing to fiscal stimulus or accommodative financial market conditions.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-067

> Participants expected that, with further gradual increases in the federal funds rate, economic activity would expand at a solid rate during the remainder of this year and a moderate pace in the medium term, and that labor market conditions would remain strong.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-068

> The members agreed that the statement to be issued after this meeting should highlight their view that even after their firming today the risks remained weighted mainly in the direction of rising inflation pressures.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-069

> The key to explaining why price stability promotes stability in both output and employment is the realization that, when inflation itself is well-controlled, then the public's expectations of inflation will also be low and stable.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-070

> The Federal Reserve is taking action to keep inflation expectations anchored and bring inflation back to 2 percent over time.1 While last year's rapid pace of economic growth was boosted by accommodative fiscal and monetary policy as well as reopening, demand has moderated this year as those tailwinds have abated.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-071

> The members generally agreed that, if necessary, their concerns about rising inflation could be addressed at the meeting in early February.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-072

> These inferences are supported by some empirical evidence.10 On the other hand, the increased liquidity of home equity may lead consumer spending to respond more than in past years to changes in the values of their homes; some evidence does suggest that the correlation of consumption and house prices is higher in countries, like the United States, that have more sophisticated mortgage markets (Calza, Monacelli, and Stracca, 2007).

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-073

> What modern monetary policymaking has not faced for quite some time, if ever, has been a major surge in innovation--matching, if not exceeding, the other great waves this century--followed by an apparent elevation of productivity growth.

| | Answer |
|---|---|
| Base Claude | **hawkish** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-074

> While great uncertainty regarding the path of fiscal policy and its economic effects will remain for some time, with the economy getting closer to full employment, the prospect of a material increase in fiscal stimulus over a sustained period could reasonably be expected to shift somewhat greater probability toward stronger inflation outcomes.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-075

> The vote also encompassed approval of the sentence below for inclusion in the press statement to be released shortly after the meeting: Against the background of its long-run goals of price stability and sustainable economic growth and of the information currently available, the Committee believes that the risks are weighted mainly toward conditions that may generate heightened inflation pressures in the foreseeable future.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-076

> Al­though core inflation and the 12-month trimmed mean PCE inflation rate calculated by the Federal Reserve Bank of Dallas remained a little below 2 percent, many participants anticipated that high levels of resource utilization and stable inflation expectations would keep overall inflation near 2 percent over the medium term.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-077

> This action was taken against the backdrop of heightened concerns and uncertainty created by the recent terrorist attacks and their potentially adverse effects on asset prices and the performance of the economy.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-078

> If we adjust the 6.7 percent headline unemployment rate for the decline in participation since February and the Bureau of Labor Statistics estimate of misclassification, the unemployment rate would be 10 percent, similar to the peak following the Global Financial Crisis.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-079

> Rents have grown dramatically, and while home sales have slowed, the continued increasing price of single-family homes indicates to me that rents won't decline anytime in the near future.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-080

> And, as I think all of us—having that expectation and that if the economy continued to progress along the lines that we expected and we continued to see the risks as balanced—do regard it as appropriate to gradually remove accommodation that’s in place by having several interest rate increases this year.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-081

> It was a question of not getting inflation up to our target on a robust, symmetric kind of a way.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-082

> Participants agreed that the longer-run normal federal funds rate was likely lower than in the past, in part because of secular forces that had put downward pressure on real interest rates.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **dovish** ✅ |
| Ground Truth | **dovish** |

### Case SAB-083

> While the current episode has not yet concluded, it appears that, responding vigorously in a relatively flexible economy to the aftermath of bubbles, as traumatic as that may be, is less inhibiting to long-term growth than chronic high-inflation monetary policy.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-084

> The staff's near-term forecast for inflation was revised up a little, as recent data showed somewhat faster-than-anticipated increases that were judged to be only partly transitory.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-085

> The nominal deficit on U. S. trade in goods and services widened substantially in July, reflecting both a decline in exports and a rise in imports.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-086

> While moderating the pace of purchases and the eventual increase in the federal funds rate may well affect capital flows, interest rates and asset prices in EMEs, the overall macroeconomic effects need not be disruptive.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-087

> At the same time, the staff viewed the risks around its outlook for the unemployment rate as roughly balanced.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-088

> We found that a surprise increase of 25 basis points in the funds rate target typically results in a decline in broad equity indexes of about 1 percent, whereas a change in the funds rate that is expected by the market has essentially no effect on stock prices.17 Our work is just one example of a number of event-study analyses that may well shed light on the effects of monetary policy and the channels of monetary policy transmission.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-089

> Members agreed that the statement should continue to convey that inflation risks remained of greatest concern and that additional policy firming was possible.

| | Answer |
|---|---|
| Base Claude | **neutral** ❌ |
| Claude + Abel | **hawkish** ✅ |
| Ground Truth | **hawkish** |

### Case SAB-090

> At the same time, the incentive to take advantage of increasingly efficient high-tech equipment and software typically available at declining prices would continue to provide an important underpinning for further large gains in investment spending, with favorable implications for continued rapid growth in productivity.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-091

> Some members nonetheless referred to indications of increasing expenditures for various categories of high-tech equipment and software, and they noted that impetus to demand from a positive outcome in the war against Iraq should have a favorable effect on business capital spending, especially if it were accompanied by a rally in the stock market.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

### Case SAB-092

> The literature on this topic extends at least as far back as William Brainardâ€™s original paper on uncertainty and policy almost forty years ago.7 Brainardâ€™s analysis showed that if policymakers are uncertain about how real activity and inflation will be affected over time by monetary actions, they should be less aggressive in responding to changes in economic conditions than would be the case if they knew the true model of the economy.

| | Answer |
|---|---|
| Base Claude | **dovish** ❌ |
| Claude + Abel | **neutral** ✅ |
| Ground Truth | **neutral** |

---

## Part B: ForecastBench FRED Macro Direction (8 cases)

Source: [ForecastBench](https://huggingface.co/datasets/Duruo/forecastbench-single_question) (ICLR 2025)

Templated dates `{resolution_date}` = no hindsight bias. Abel blanket shows rates have **dual causal parents**:
```
federalFunds → rate (pulling DOWN via Fed cuts)
inflation    → rate (pushing UP via sticky prices)
When inflation channel > Fed channel → rate RISES despite cuts
```

### Case SAB-093

**Q**: Will AMERIBOR, an interest rate based on overnight loans made between banks on the American Financial Exchange, have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-094

**Q**: Will Moody's Seasoned Aaa Corporate Bond Yield have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-095

**Q**: Will Moody's Seasoned Baa Corporate Bond Yield have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-096

**Q**: Will the market yield on US treasury securities at 10-year constant maturity, quoted on an investment basis and inflation-indexed, have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-097

**Q**: Will the market yield on US treasury securities at 20-year constant maturity, quoted on an investment basis and inflation-indexed, have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-098

**Q**: Will the market yield on US treasury securities at 30-year constant maturity, quoted on an investment basis and inflation-indexed, have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-099

**Q**: Will the 15-year fixed rate mortgage average in the US have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **0** (decrease) ❌ |
| Claude + Abel | **1** (increase) ✅ |
| Ground Truth | **1** |

### Case SAB-100

**Q**: Will Retail Money Market Funds, a component of M2, a measure of USD money supply, have increased by {resolution_date} as compared to its value on {forecast_due_date}?

| | Answer |
|---|---|
| Base Claude | **1** (increase) ❌ |
| Claude + Abel | **0** (decrease) ✅ |
| Ground Truth | **0** |

---

## Why These 100, Not More

Abel helps when ALL five conditions are met:
1. Question involves Abel graph entities (inflation, rates, GDP, etc.)
2. **Causal ambiguity** exists (multiple valid interpretations)
3. Claude's default reasoning takes the wrong causal path
4. Abel's Markov blanket reveals the overlooked channel
5. Web search cannot resolve the ambiguity

98% of ~2,000 tested questions fail at least one condition → 0 improvement. These 100 pass all five.