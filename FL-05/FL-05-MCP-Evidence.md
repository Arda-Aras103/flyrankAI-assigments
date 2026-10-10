# FL-05 — MCP Connector Evidence

**Date:** 10 October 2026  
**MCP client:** Codex desktop  
**Connector:** `mcp__node_repl__js` (Node REPL tool bridge)  
**Scope:** Read-only inspection of local FL-04 deliverables. No external account or Claude configuration was changed.

The three tasks below were run as successful connector calls in this Codex conversation. Their call IDs let a reviewer match each record to the call history. The rendered transcript is also available as [FL-05-MCP-Execution-Transcript.html](FL-05-MCP-Execution-Transcript.html).

## Task 1 — Inspect FL-04 workflow stages

**Call ID:** `exec-660433fe-81f8-4acf-b54c-4bf733ca7b3d`  
**Request:** Read the local workflow configuration and list its Markdown headings.

**Tool code:**

```js
let fs1 = await import('node:fs/promises');
let p1 = `${nodeRepl.cwd}/outputs/FL-04-Workflow-Configuration-v2.md`;
let s1 = await fs1.readFile(p1, 'utf8');
nodeRepl.write(s1.split(/\r?\n/).filter(x => /^#{1,4}\s/.test(x)).join('\n'));
```

**Returned output:**

```text
# FL-04 — Opportunity Triage Workflow v2
## Persistent instructions
### Purpose
### Profile to verify before use
### Evidence rules
### Decision rules
## Run prompts
### Prompt 1 — Gather evidence
### Prompt 2 — Synthesize against the profile
### Prompt 3 — Critique and correct
### Prompt 4 — Format the final brief
## Human handoff
```

## Task 2 — Audit the five FL-04 runs

**Call ID:** `exec-351e525f-12fe-4f11-884e-852b25a80454`  
**Request:** Read the local walkthrough and extract the run headings and decision marks.

**Tool code:**

```js
let fs2 = await import('node:fs/promises');
let p2 = `${nodeRepl.cwd}/outputs/FL-04-Walkthrough-v2.md`;
let s2 = await fs2.readFile(p2, 'utf8');
nodeRepl.write(s2.split(/\r?\n/).filter(x =>
  /^#{1,4}\s/.test(x) || /\b(KEEP|REVIEW|SKIP)\b|Final mark|Final decision/i.test(x)
).slice(0, 90).join('\n'));
```

**Returned results:**

| Run | Opportunity | Final mark |
|---:|---|---|
| 1 | Baykar, 2027 Spring Internship — DevOps | REVIEW |
| 2 | Baykar, 2027 Spring Internship — Object-Oriented Software | REVIEW |
| 3 | Baykar, 2027 Spring Internship — AI Software Development | REVIEW |
| 4 | Microsoft, Software Engineering Intern — Belgrade | SKIP |
| 5 | Microsoft, Software Engineering Internship Opportunities — CoreAI, Prague | SKIP |

## Task 3 — Verify the source links

**Call ID:** `exec-52577a08-dbdc-407d-8c79-796b6fd43efd`  
**Request:** Read the walkthrough, parse Markdown links, and count them by host.

**Tool code:**

```js
let fs3 = await import('node:fs/promises');
let p3 = `${nodeRepl.cwd}/outputs/FL-04-Walkthrough-v2.md`;
let s3 = await fs3.readFile(p3, 'utf8');
let urls3 = [...s3.matchAll(/\[[^\]]+\]\((https?:\/\/[^)\s]+)\)/g)].map(m => m[1]);
let hosts3 = {};
for (let u of urls3) {
  let h = new URL(u).hostname;
  hosts3[h] = (hosts3[h] || 0) + 1;
}
nodeRepl.write(JSON.stringify({markdownLinks: urls3.length, hosts: hosts3, sample: urls3.slice(0, 3)}, null, 2));
```

**Returned output:**

```json
{
  "markdownLinks": 14,
  "hosts": {
    "kariyer.baykartech.com": 6,
    "apply.careers.microsoft.com": 4,
    "careers.microsoft.com": 4
  },
  "sample": [
    "https://kariyer.baykartech.com/tr/acik-pozisyonlar/detay/2027-bahar-donemi-staj-devops",
    "https://kariyer.baykartech.com/tr/acik-pozisyonlar/detay/2027-bahar-donemi-staj-devops",
    "https://kariyer.baykartech.com/tr/acik-pozisyonlar/detay/2027-bahar-donemi-staj-nesne-tabanli-yazilim"
  ]
}
```

## Screenshot evidence

The following genuine screenshots were captured from the expanded Codex activity history. Each shows the corresponding MCP task and its returned output. The HTML transcript is supplementary; these images are direct captures of the tool activity in the Codex UI.

- [Task 1 — inspect FL-04 stage headings](FL-05-MCP-task-1.jpg)
- [Task 2 — audit the five FL-04 runs](FL-05-MCP-task-2.jpg)
- [Task 3 — verify the source links](FL-05-MCP-task-3.jpg)

## Connector limits

- The Node REPL connector read local files; no Claude account or third-party MCP server was configured.
- Extracted labels and links are a useful audit aid, not proof that a job is still open or that the source content is current.
- A human must open the official posting, verify its status and eligibility, and make the final opportunity decision.
