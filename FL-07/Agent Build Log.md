# FL-07 — Agent Build Log

## 16 October 2026 — first build pass

### Starting point

FL-06 selected an Opportunity Scout for FlyRank and self-hosted n8n. It should triage one opportunity at a time, use a public source, and recommend a human-reviewed next step without taking external action.

### What I changed while building

1. **Checked the runtime before writing the workflow.** The available project copy is on Windows. Docker and npm/n8n are not installed here; WSL returns `Wsl/E_ACCESSDENIED`. I could not start the chosen n8n platform in this session.
2. **Narrowed the research tool.** The first design allowed up to two URLs and left more room for the model to choose a URL. For this MVP I reduced that to one submitted HTTPS URL, validated before the agent runs, and bound the HTTP tool to that exact validated URL. This is simpler to inspect and limits what the model can request.
3. **Kept only the core job.** No search engine, multi-source reconciliation, persistence, CRM, messaging, or automated acceptance. They add setup and failure modes before one triage run has been verified.
4. **Made the tool read-only.** It uses GET without authentication, credentials, request body, or write capability. Local n8n is loopback-bound and SSRF protection is enabled in the supplied Compose file. n8n documents SSRF protection as defense in depth and still recommends network-level controls.
5. **Prepared an importable workflow rather than claiming a live run.** `Opportunity Scout.json` contains the form, URL validation, AI Agent, HTTP tool, model connection placeholder, and final report node. The OpenAI credential must be set in n8n after import.

### What broke / current blockers

- The project repo has filenames with `:` and `?`, which Windows cannot check out as ordinary files. The local clone therefore has an incomplete working tree. I used Git object content to inspect the FL-06 specification and kept this change in new Windows-safe FL-07 paths.
- Docker is unavailable and WSL is access-denied, so n8n could not be started and the workflow could not be imported or executed in this environment.
- No OpenAI credential is available in the current n8n instance because no instance is running. No API key was added to files.

### Cut from the spec and why

- **Two source URLs → one URL:** smaller tool surface for the first version; can add a second fixed source after a successful run.
- **Autonomous search → user-submitted source only:** the goal is one bounded triage, not a broad scout that can wander across sites.
- **Raw two-minute capture → deferred:** a recording of a successful run cannot be made honestly before the workflow has actually run. The capture is still outstanding.
- **Five executed eval runs → cases prepared, execution deferred:** the five expected behaviors are defined in `Build the Agent.md`; the n8n runtime is the missing dependency. No outputs are fabricated.

### What is verified vs. unverified

- **Verified in this build pass:** FL-06 scope inspected; workflow structure and prompts written; JSON syntax and basic graph references checked before commit.
- **Not verified:** n8n import compatibility, credential connection, form submission, live HTTP tool call, agent output quality, output page behavior, and the five evaluation cases.

### Time accounting

- Actual hands-on time in this session was not measured with a stopwatch; do not claim a time-saved figure from this build pass.
- No manual-vs-agent comparison or five-run average exists yet. After the first working run, time five inputs and compare total human minutes against doing those same inputs manually. Include setup time separately.

### First-run checklist when Docker/WSL is available

1. Run `docker compose up -d` from `FL-07/`.
2. Open `http://localhost:5678`, finish n8n owner setup, and import `Opportunity Scout.json`.
3. Select an OpenAI credential in the OpenAI Chat Model node; do not paste keys into the prompt or JSON export.
4. Confirm the Form Trigger requires a logged-in n8n user and the instance remains local.
5. Test invalid URL rejection first (`http://localhost` and a private IP should fail before the model node).
6. Run a live official public URL through the Test form. Confirm the execution shows the HTTP Request Tool call and the `Return Report` node has a report plus the same source URL.
7. Run each of the five pre-build evaluation cases, note actual outputs and pass/fail, and revise the prompt only when a concrete failure appears.
8. Capture one unedited, roughly two-minute screen recording from form submission through the final execution output. Add the raw file beside this log only after recording it.

## Known failure points and human checks

- **Unreachable or script-rendered source:** the agent may see little readable page text. It must disclose this and use insufficient evidence; a human can paste an official excerpt in a later version.
- **Stale or promotional content:** the page may be outdated or biased. Human must verify that it is current and official.
- **URL/network edge cases:** URL string checks alone cannot resolve every DNS or redirect risk. The included n8n SSRF defense is defense in depth; keep the service local and add network egress controls before any public deployment.
- **Model overclaiming:** source citations do not prove every inference. Human checks material claims and uncertainty.
- **Sensitive input:** the description, criteria, and fetched page content go to the model provider. Do not submit confidential or personal client data.
- **Decision risk:** priority is advice. The human verifies fit and takes every consequential action.
