# FL-02 Prompt Iteration Log

**Task (from FL-01):** Summarizing opportunities — I paste a job / internship / scholarship / program and need a keep-or-skip call I can review in seconds.

**Why this task:** FL-01 said I delegate this with review. A wrong yes wastes time next to FlyRank, AWS SBG, and GCAF.

**Fixed input for every version** (same posting, so only the prompt changes):

```
Company: CloudForge
Role: Junior DevOps Intern
Location: Remote, EU timezone preferred. US work authorization required.
Dates: 10 hours/week, overlaps my current programs.
Source: internships-daily.com roundup (not the company site).
Stack: Docker, some AWS, Terraform mentioned once.
Pay: unpaid.
Apply: form on the roundup site.
```

Voice card: direct, plain, specific, short, explanatory, no buzzwords.

---

## V0 — naive (baseline)

**Technique:** none

**Prompt**

```
Is this internship good?
```

**Output**

> It depends on your goals! Unpaid internships can still be valuable for experience. Docker and AWS are in-demand skills. Remote work is a plus. I'd say go for it if you have the time.

**What changed in the output:** nothing to compare.

**What still failed:** No verdict. Ignored unpaid, US-auth, unofficial source, and my load.

---

## V1 — role assignment

**Technique:** role assignment

**Prompt**

```
You are a career advisor for a computer engineering student.
Is this internship good?
```

**Output**

> As your advisor, I would treat this as a maybe. The stack is relevant, but unpaid roles should be weighed against your studies. Check if they can sponsor or if the US authorization rule blocks you. Remote is convenient.

**Observed difference:** It started hedging about unpaid and authorization. Still no kill/keep. “Career advisor” added soft talk, not a decision.

**Why:** Role without my rules just changes the costume.

---

## V2 — context and motivation

**Technique:** context and motivation

**Prompt**

```
You are a career advisor for a computer engineering student.

Context: I am Arda, 3rd year, Ege University, graduating 2028.
I want Cloud / Backend / DevOps / GenAI engineering.
I can do Izmir office, hybrid, Turkey remote, or abroad remote.
English applications are fine.
I already carry FlyRank, AWS SBG, and GCAF. A light overlap is acceptable.
Unpaid is allowed only if the work is clearly technical.
Motivation: I need a keep-or-skip so I do not spend an evening on a posting that will reject me or eat the week.

Is this internship good?
```

**Output**

> Skip or be very careful. US work authorization likely knocks you out from Turkey. The source is a roundup, not CloudForge. Unpaid plus 10 hours on top of three programs is possible but not free. The stack fits. Confirm the real careers page before anything else.

**Observed difference:** It used my constraints. Authorization and the scrape site showed up. Still a paragraph, still “be careful,” not a label.

**Why:** Context is what actually moved the answer. Role alone did not.

---

## V3 — few-shot examples

**Technique:** few-shot examples

**Prompt**

```
You are a career advisor for a computer engineering student.

Context: I am Arda, 3rd year, Ege University, graduating 2028.
I want Cloud / Backend / DevOps / GenAI engineering.
I can do Izmir office, hybrid, Turkey remote, or abroad remote.
English applications are fine.
I already carry FlyRank, AWS SBG, and GCAF. A light overlap is acceptable.
Unpaid is allowed only if the work is clearly technical.
Motivation: I need a keep-or-skip so I do not spend an evening on a posting that will reject me or eat the week.

Examples:
1) Official AWS internship, remote, student-eligible, paid, Terraform/Linux → ✅ because field, status, and source all pass.
2) Marketing intern, Istanbul, paid → ❌ because not Cloud/Backend/DevOps/GenAI.
3) “DevOps intern” on a scrape blog, US citizens only, unpaid → ❌ because authorization and source.

Is this internship good?
```

**Output**

> This is example 3. ❌
> US work authorization, unofficial roundup, unpaid. Stack fit is not enough.

**Observed difference:** It stopped essay-writing and matched a labeled example. First hard ❌.

**Why:** The examples taught the decision shape better than another sentence of context.

---

## V4 — output structure

**Technique:** output structure

**Prompt**

```
You are a career advisor for a computer engineering student.

Context: I am Arda, 3rd year, Ege University, graduating 2028.
I want Cloud / Backend / DevOps / GenAI engineering.
I can do Izmir office, hybrid, Turkey remote, or abroad remote.
English applications are fine.
I already carry FlyRank, AWS SBG, and GCAF. A light overlap is acceptable.
Unpaid is allowed only if the work is clearly technical.
Motivation: I need a keep-or-skip so I do not spend an evening on a posting that will reject me or eat the week.

Examples:
1) Official AWS internship, remote, student-eligible, paid, Terraform/Linux → ✅ because field, status, and source all pass.
2) Marketing intern, Istanbul, paid → ❌ because not Cloud/Backend/DevOps/GenAI.
3) “DevOps intern” on a scrape blog, US citizens only, unpaid → ❌ because authorization and source.

Is this internship good?

Output exactly:
- Mark: ✅ or ⚠️ or ❌
- Field:
- Eligibility:
- Time:
- Source:
- One or two sentences. No extra sections.
```

**Output**

> - Mark: ❌
> - Field: pass (Docker / AWS / Terraform)
> - Eligibility: fail (US work authorization)
> - Time: manageable (10h, overlap allowed)
> - Source: fail (internships-daily.com, not company)
> - Skip. Authorization and the scrape site are enough. Do not fill the roundup form.

**Observed difference:** Same verdict, now I can see which check killed it. Time was not treated as an automatic no.

**Why:** Structure made the four FL-01 checks visible instead of melted into a vibe.

---

## V5 — step decomposition

**Technique:** step decomposition

**Prompt**

```
You are a career advisor for a computer engineering student.

Context: I am Arda, 3rd year, Ege University, graduating 2028.
I want Cloud / Backend / DevOps / GenAI engineering.
I can do Izmir office, hybrid, Turkey remote, or abroad remote.
English applications are fine.
I already carry FlyRank, AWS SBG, and GCAF. A light overlap is acceptable.
Unpaid is allowed only if the work is clearly technical.
Motivation: I need a keep-or-skip so I do not spend an evening on a posting that will reject me or eat the week.

Examples:
1) Official AWS internship, remote, student-eligible, paid, Terraform/Linux → ✅ because field, status, and source all pass.
2) Marketing intern, Istanbul, paid → ❌ because not Cloud/Backend/DevOps/GenAI.
3) “DevOps intern” on a scrape blog, US citizens only, unpaid → ❌ because authorization and source.

Is this internship good?

Do this in order, then output only the final block:
1. Score field (Cloud / Backend / DevOps / GenAI).
2. Score eligibility (geo / status / work authorization).
3. Score time against FlyRank, AWS SBG, GCAF. Overlap is not an automatic no.
4. Score source (official page vs scrape / SEO roundup).
5. If eligibility or source fails → ❌. If only time is tight → ⚠️. If all pass → ✅.

Output exactly:
- Mark: ✅ or ⚠️ or ❌
- Field:
- Eligibility:
- Time:
- Source:
- One or two sentences. No extra sections.
```

**Output**

> - Mark: ❌
> - Field: pass
> - Eligibility: fail (US work authorization required)
> - Time: pass (10h, overlap allowed)
> - Source: fail (roundup, not CloudForge)
> - Skip. Two failing checks. Do not apply on internships-daily.com.

**Observed difference:** Same ❌, but the rule “eligibility or source fail → ❌” is explicit. Less chance it upgrades a blocked posting to ⚠️ because the stack looks nice.

**Why:** Decomposition locked the decision order. Helpful, smaller jump than V2 or V3.

---

## Cross-model comparison

**Final prompt:** V5 + the CloudForge input. Ran on Claude and ChatGPT.

**ChatGPT (raw)**

> - Mark: ❌
> - Field: DevOps — Docker, AWS, Terraform.
> - Eligibility: ❌ US work authorization required, so you are not eligible.
> - Time: ⚠️ 10 hrs/week overlaps FlyRank, AWS SBG, and GCAF.
> - Source: ❌ SEO/roundup site, not the company’s official posting.
> - Even aside from the time overlap and unpaid status, the US work-authorization requirement and non-official source make this a skip.

**Claude (raw)**

> - Mark: ❌
> - Field: Pass, DevOps stack (Docker, AWS, Terraform).
> - Eligibility: Fail, requires US work authorization you don't have.
> - Time: Light overlap, acceptable on its own.
> - Source: Fail, third-party roundup site, not the company's own page, apply form isn't official either.
> - Two independent fails (eligibility, source) means skip this one, don't spend the evening on it.

|                | Claude                                                             | ChatGPT                                                                                   |
| -------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| Tone           | Short, dry, stayed on the four checks                              | Same mark, but argued extra (unpaid, time as a problem)                                   |
| Accuracy       | Followed step 3: overlap is not an automatic no. Time = acceptable | Broke step 3. Marked Time ⚠️ even though the prompt said light overlap is fine            |
| Structure      | Pass/fail words + one kill sentence                                | Put ✅❌⚠️ on the sub-rows, which the template reserved for the final mark                |
| Failure points | Did not mention unpaid. Clean skip                                 | Dragged unpaid into the closer. Would make a 10h official paid role look worse than it is |

Same final mark (❌). They split on **time**. Claude used the written rule. ChatGPT used a vibe. For this template, Claude is the one to copy.

---

## Final reusable template

A stranger can fill the braces. No Arda-only facts baked in.

```
You are reviewing one {job / internship / scholarship / program} for a student targeting {fields}.

Constraints:
- Locations they can do: {list}
- Current load: {programs}. Light overlap is acceptable.
- Unpaid is OK only if the work is clearly {technical / not}.

Examples:
- {one clear yes}
- {one clear no for field}
- {one clear no for eligibility or source}

Do this in order, then output only the final block:
1. Field fit
2. Eligibility (geo / status / authorization)
3. Time vs current load
4. Source (official vs scrape)
5. If eligibility or source fails → ❌. If only time is tight → ⚠️. If all pass → ✅.

Output exactly:
- Mark: ✅ or ⚠️ or ❌
- Field:
- Eligibility:
- Time:
- Source:
- One or two sentences. No extra sections.

Posting:
{paste}
```

---

## What actually earned a place

| Version | Technique              | Output change                                 |
| ------- | ---------------------- | --------------------------------------------- |
| V0      | none                   | Soft “it depends”                             |
| V1      | role assignment        | Slightly more cautious, still no decision     |
| V2      | context and motivation | Used my constraints; first real skip language |
| V3      | few-shot               | Hard ❌, matched example 3                    |
| V4      | output structure       | Four checks visible                           |
| V5      | step decomposition     | Fail rule explicit                            |

Weakest add: **role assignment**. Strongest: **context** then **few-shot**.
