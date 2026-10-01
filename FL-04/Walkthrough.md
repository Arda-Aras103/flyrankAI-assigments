# FL-04 — Ship an Automation Workflow v2

**Track:** General AI Fluency · **Phase:** Build (core) · **Workflow:** Opportunity Triage v1.0  
**Selected from audit:** Summarizing opportunities — FL-01 delegates this with review; FL-02 identifies the task as a keep-or-skip call for jobs, internships, scholarships, and programs.  
**Research snapshot date:** 1 October 2026

## What I built

A no-code, four-prompt workflow for screening one opportunity at a time. It runs in a ChatGPT/Claude conversation with web access; the reusable Project/GPT instructions and all stage prompts are in [Workflow Configuration.md](Workflow%20Configuration.md). It carries forward the constraints and decision rules recorded in FL-02, instead of asking the model to guess what “good” means.

The run ends with a concise, source-linked mark and a human check. No application is submitted and no personal data is sent.

## Flow diagram

```text
New opportunity link
  → 1. Gather: verify official source and extract facts
  → Evidence Card
  → 2. Synthesize: compare field / eligibility / time / source / pay
  → Proposed Decision
  → 3. Critique: try to disprove the mark and remove unsupported claims
  → Corrected Decision
  → 4. Format: fixed seven-field brief
  → Human verifies the official page and decides
```

The handoff is the complete prior stage output, including its source links. The workflow fails closed to ⚠️ when a material fact is unknown; ❌ is reserved for a clear hard failure such as an expired cycle, stated location conflict, or field mismatch.

## Five real runs

Each run below used a real opportunity page, browsed on 1 October 2026. The source snapshot supports the notes; application status can change after that date. The final brief is the output of the gather → synthesize → critique → format process, with human review noted separately.

### Run 1 — Vidco Yazılım, Software Intern

**Input:** [Vidco careers page](https://www.vidco.com.tr/kariyer)  
**Evidence gathered:** The employer page says that, as of 10 September 2026, a Software Intern role is open, remote, with no residence requirement. It asks candidates to email a CV. It does not state the duties, schedule, term, pay, degree/year, or application deadline.  
**Final brief:**

```text
- Mark: ⚠️ REVIEW
- Field: partial — software internship is relevant, but the technical area and duties are not stated.
- Eligibility: pass on stated location; degree/year requirements are not stated.
- Time: unknown — hours and duration are not stated.
- Source: official employer careers page, checked 1 Oct 2026 — https://www.vidco.com.tr/kariyer
- Missing check: Ask whether the internship work is technical, what the weekly schedule/duration is, and whether it is paid.
- Action: Email only after confirming the duties, schedule, and compensation; the posting requests a CV by email.
```

**Review note:** Remote/no-residence fit is supported; “software intern” alone is not enough to satisfy the unpaid-work rule. Pay is not stated, so this is not treated as unpaid.

### Run 2 — Baykar, 2027 Spring Internship | DevOps

**Input:** [Baykar DevOps internship](https://kariyer.baykartech.com/en/acik-pozisyonlar/detay/2027-bahar-donemi-staj-devops)  
**Evidence gathered:** Official page describes CI/CD and automation in AWS/Huawei Cloud environments, Docker, monitoring/logging, and scripting. It does not state a deadline, location/work mode, weekly schedule, duration, or compensation on the page inspected.  
**Final brief:**

```text
- Mark: ⚠️ REVIEW
- Field: pass — direct DevOps, cloud, CI/CD, automation, and observability duties.
- Eligibility: unknown — the page inspected does not state class/year or location/work-mode requirements.
- Time: unknown — weekly hours, schedule, and duration are not stated.
- Source: official Baykar careers page, checked 1 Oct 2026 — https://kariyer.baykartech.com/en/acik-pozisyonlar/detay/2027-bahar-donemi-staj-devops
- Missing check: Confirm application deadline, location/work mode, eligible year, duration, hours, and compensation in the apply flow.
- Action: Keep it on the shortlist, then verify the application form before investing in an application.
```

**Review note:** Strong field fit did not promote the result to ✅ because core eligibility and timing remain unknown.

### Run 3 — Baykar, 2027 Spring Internship | Object-Oriented Software

**Input:** [Baykar Object-Oriented Software internship](https://kariyer.baykartech.com/tr/acik-pozisyonlar/detay/2027-bahar-donemi-staj-nesne-tabanli-yazilim)  
**Evidence gathered:** The official page accepts third- or fourth-year students or recent graduates from specified engineering disciplines. Work areas listed span desktop, server, distributed systems, DevOps, testing, data tools, and web; it does not promise an assignment to a particular area or state schedule/pay/deadline in the inspected text.  
**Final brief:**

```text
- Mark: ⚠️ REVIEW
- Field: partial — relevant software and DevOps areas are listed, but team/project placement is unspecified.
- Eligibility: pass on the stated class/discipline rule if the saved third-year profile is current.
- Time: unknown — hours, duration, and work mode are not stated.
- Source: official Baykar careers page, checked 1 Oct 2026 — https://kariyer.baykartech.com/tr/acik-pozisyonlar/detay/2027-bahar-donemi-staj-nesne-tabanli-yazilim
- Missing check: Confirm the specific team/project, location, application deadline, schedule, and compensation.
- Action: Review the role details before applying; ask whether a DevOps/backend assignment is available.
```

**Review note:** The project match cannot be inferred from a broad list of possible work areas.

### Run 4 — Tenstorrent, Software Engineering Intern (October 2026 start)

**Input:** [Tenstorrent University Jobs](https://job-boards.greenhouse.io/tenstorrentuniversity/jobs/5221670007)  
**Evidence gathered:** The official application page lists Belgrade, Serbia; onsite work; October 2026–January 2027; and systems software using C++, Python, Linux, testing, and debugging. The application form asks whether candidates can work in the office five days a week. It also says the offer depends on eligibility to access U.S. export-controlled technology. The saved profile allows abroad remote work, not onsite relocation abroad.  
**Final brief:**

```text
- Mark: ❌ SKIP
- Field: partial — systems software is technical, but it is outside the stated Cloud/Backend/DevOps/GenAI target list.
- Eligibility: fail on stated work mode/location — the role is onsite in Belgrade, while the saved profile does not include onsite relocation abroad; export-control eligibility is also unresolved.
- Time: unknown — term is Oct 2026–Jan 2027; weekly hours are not stated.
- Source: official Tenstorrent application page, checked 1 Oct 2026 — https://job-boards.greenhouse.io/tenstorrentuniversity/jobs/5221670007
- Missing check: None for the current profile/location decision; export-control eligibility would require direct employer clarification if the location constraint changes.
- Action: Skip under the current location constraints; do not infer export-control eligibility from nationality or residence.
```

**Review note:** Location is sufficient for the current skip. The workflow must not make a legal conclusion about export rules.

### Run 5 — Siemens Türkiye, Summer Internship 2026

**Input:** [Siemens Türkiye internships](https://www.siemens.com/en-gb/company/jobs/growth-careers/internships-turkey/)  
**Evidence gathered:** The official page says applications are accepted 1–28 February and, for undergraduate applicants, the internship must be mandatory and students must be completing their third or fourth year in summer 2026. That application window and cycle have passed as of the research snapshot date.  
**Final brief:**

```text
- Mark: ❌ SKIP
- Field: unknown — the page describes a general internship program and does not specify a role/team for this input.
- Eligibility: unknown for a future cycle; current 2026 cycle is closed.
- Time: not applicable to a closed cycle.
- Source: official Siemens Türkiye page, checked 1 Oct 2026 — https://www.siemens.com/en-gb/company/jobs/growth-careers/internships-turkey/
- Missing check: For the next cycle, recheck dates, role/team, mandatory-internship requirement, and class/year rule.
- Action: Do not apply to the 2026 cycle; check the official page when Siemens publishes the next application window.
```

**Review note:** A closed opportunity is not called a poor-quality role; it is not actionable for this cycle.

## Time accounting

I did not have the student’s live stopwatch baseline while preparing this artifact, so the figures below are explicit planning estimates, not claimed stopwatch measurements. Replace them with actual user timings during the next five runs.

| Work | Manual baseline | Workflow-assisted estimate |
|---|---:|---:|
| One posting: locate official page, read it, compare against constraints, write a short decision | 15 min | 5 min human time (paste URL, inspect output, verify official page) |
| Five postings | 75 min | 25 min run time + 20 min one-time Project setup = 45 min |
| Net after five runs | — | **30 min saved** |

**Break-even:** Setup cost is recovered after two postings (20 ÷ (15 − 5) = 2). This estimate does not count model response latency as human time. On the first real use, time one manual posting and one assisted posting; then replace this table with those observations.

## Where it breaks and what a human must check

- **Stale or missing dates:** Search results and career pages can be out of date. Open the official page immediately before applying and verify the current cycle/deadline.
- **Hidden application requirements:** Some role eligibility, schedule, pay, or location details appear only in the apply form. The assistant must use ⚠️ until those fields are checked.
- **Broad role descriptions:** Baykar's Object-Oriented Software listing names many possible areas. A list of technologies does not prove the intern will work in the preferred team; ask the recruiter.
- **Ambiguous role labels:** “Software Intern” does not establish that the work is technical enough to qualify for unpaid work. Confirm duties before proceeding.
- **Export-control and work authorization:** The model can surface a stated condition but cannot decide legal eligibility. Ask the employer or a qualified adviser; never infer eligibility from country or nationality.
- **Profile drift:** Grade, graduation date, current programs, and location preferences can change. Update the persistent profile before a new batch.
- **Source identity:** A polished page may not be an employer's official page. Confirm the domain and follow links from the employer's own careers site.

**Human must still check:** official source, live application status/deadline, exact eligibility and work authorization, on-site/remote requirements, schedule and workload, compensation, and whether duties match the student's technical goals. The human makes the final apply/skip choice.

## Build and run notes

- No code, API keys, or automated application actions are part of this workflow.
- To run on a brand-new input: open a fresh conversation with the Project instructions, paste the new URL into Prompt 1, then pass each output to the next prompt. The five source pages above were separate end-to-end inputs.
- I used the same fixed output schema across all five runs; uncertainty was kept visible instead of being filled with guesses.
- GitHub repository context: [flyrankAI-assigments](https://github.com/Arda-Aras103/flyrankAI-assigments). The workflow was selected from the local FL-01 audit and FL-02 prompt iteration notes.
