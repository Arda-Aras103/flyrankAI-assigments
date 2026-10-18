# Survive the Crit — AI Preflight and Local Revision

**Assignment:** Week 6 · Build+  
**Review type:** AI-only preflight; no human reviewer was available. No human feedback is claimed in this report.  
**Site status:** Candidate edits are saved in a likely local source folder and were visually previewed. They have not been deployed, so the live portfolio is unchanged.

## Chapter 1 proof statement

> I can build practical command-line tools in Go that solve real developer and system-workflow problems. I am proving this to a hiring manager looking for a junior DevOps, Cloud, or Software Engineer who values practical engineering ability, and the single action I want them to take is to review my CV and consider me for an interview.

## AI preflight of the live portfolio before edits

The live homepage opened with “Backend systems, built around real data.” It described databases, APIs, cloud tools, and an AI workflow. Its project list did not show the Go command-line work named in the proof statement. The main hero action was “Explore my work”; the CV link was less prominent.

### AI ten-second read — not a human response

- **What I think Arda does:** Builds backend software around databases and APIs, with an AI opportunity-triage project.
- **Would I believe he is good at it?** Partly. The Task API and opportunity-triage descriptions provide some evidence, but the page did not show the Go CLI work or foreground the requested CV action.
- **Confidence and limit:** This is my reading of the page, not a real reviewer’s answer. It cannot satisfy the assignment’s human-feedback requirement.

## AI-identified priorities and local changes

This is an AI priority sort, not a sort of reviewer feedback.

| Priority | Finding | Candidate change | State |
|---|---|---|---|
| Must-fix | The proof statement is about practical Go command-line tools, but the live homepage led with backend systems and did not show that Go work. | Added the Project Euler Go work as the first project and updated the headline and supporting copy to name Go CLI tools and backends. | Saved locally; not deployed. |
| Must-fix | The stated next action is to review the CV, while the hero emphasized exploring projects. | Made “Review my CV” the primary hero and header action; kept “See selected work” as the secondary action. | Saved locally; not deployed. |
| Nice-to-have | The Go project description could be even easier to verify with a short README excerpt or a result from running the commands. | Consider adding only after checking the repository README and actual run output. | Later; no evidence invented. |

## Visual check of the edited local draft

I opened the local `index.html` and `cv.html` in a browser and inspected the hero, selected-work section, and CV work section.

- The homepage opens with “Go tools. Useful backends.” and explains the Go CLI/API focus.
- “Review my CV” is the primary call to action, with “See selected work” alongside it.
- “Project Euler tools in Go” is the first project card. Its description, tags, and commands are visible in the local preview.
- The CV includes the same Go project under “Selected Work.”

This verifies the local draft’s visible content and layout only. It does not verify a live deployment or prove the project commands were run during this review.

## What is and is not complete

- The candidate copy changes are present in the likely source folder: `C:\Users\cavdu\Documents\Codex\2026-10-10\https-github-com-arda-aras103-flyrankai\outputs\Arda Portfolio`.
- A human reviewer did not review the live site; the two required questions were not asked to a person and there are no human feedback quotes to sort.
- The changed draft has not been deployed. The active Netlify source is unconfirmed because the current live markup differs from this local copy in its CV routes and Netlify form markup.
- Therefore this is an honest AI preflight and local revision record, not a completed human-review checkpoint or evidence of live fixes.

## Sources

- Live portfolio: https://arda-aras-cavdur.netlify.app/
- Go project: https://github.com/Arda-Aras103/project-euler
- Chapter 1 proof statement: `Assigments/What Are You Proving?.md` in the supplied GitHub repository.
- Assignment instructions: https://aifluency.flyrank.ai/week-07.html#survive-the-crit
