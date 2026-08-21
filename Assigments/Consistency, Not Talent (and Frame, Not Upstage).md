# Week 3 — Consistency, not talent

**Claim:** I want a junior DevOps, cloud, or engineering interview. Here is what I have run.

**One action:** email cavduraras103@gmail.com and I will send the CV.

**Voice:** direct, plain, specific, short, explanatory, no buzzwords.

Repos on https://github.com/Arda-Aras103

| Repo                         | What it actually is                                                  | On the site?                  |
| ---------------------------- | -------------------------------------------------------------------- | ----------------------------- |
| visualize-git-contributions  | Go CLI (gitviz). Local commit calendar. No extra deps. Releases.     | Lead case                     |
| project-euler                | First 10 Euler problems in Go, tests/bench from 4 on                 | Second case                   |
| flyrankAI-assigments / BE-01 | FastAPI in-memory Task API                                           | Third case                    |
| url-shortener                | Gin + SQLite started. main never starts the server. Handlers unused. | No                            |
| Gemini_BBVA_Project          | Stated as a Gemini + Go + Ansible remediator. Thin README.           | Not yet                       |
| Arda-Aras103.github.io       | Hugo + PaperMod. Blog, resume, Notion templates.                     | The existing frame — strip it |

---

## Content map

Every CTA ladders to the email.

### Home

1. Claim
2. One line: I write small Go programs you can clone and run
3. Three cards — gitviz, Euler, Task API
4. CTA: Email me for the CV

### Projects / gitviz

1. Problem
2. What I did
3. What came of it
4. Real capture: terminal calendar
5. CTA: https://github.com/Arda-Aras103/visualize-git-contributions

### Projects / Project Euler

1. Problem
2. What I did
3. What came of it
4. Real capture: go test -bench=. on problem7
5. CTA: https://github.com/Arda-Aras103/project-euler

### Projects / Task API

1. Problem
2. What I did
3. What came of it
4. Real capture: Swagger /docs
5. CTA: https://github.com/Arda-Aras103/flyrankAI-assigments/tree/main/BE-01

### About

1. CS student, Ege University, class of 2028, Izmir
2. What I am proving: Go tools and small services I run
3. What I am not claiming: url-shortener is unfinished; BBVA is not framed yet
4. CTA: Email

### Contact

1. Email: cavduraras103@gmail.com
2. GitHub: https://github.com/Arda-Aras103
3. LinkedIn: https://www.linkedin.com/in/arda-aras-cavdur/
4. CTA: Send the CV

Do not put Notion templates on the DevOps path.

### Still need to gather

- A real gitviz terminal screenshot
- Cropped Swagger screenshot
- A short interview on Gemini_BBVA_Project before it becomes a case
- Optional real photo
- Not needed: AI hero, designed logo, url-shortener card

---

## Identity kit

The live site is PaperMod dark + DevOps Enthusiast + Notion templates. That is a theme, not an identity.

**Fonts**

- IBM Plex Sans — headings and body
- IBM Plex Mono — commands, bench, calendar

**Palette**

| Role        | Hex     |
| ----------- | ------- |
| Text        | #111111 |
| Background  | #F6F4EF |
| Accent      | #215A4C |
| Code ground | #ECE8E1 |

**Logo:** none.
**Favicon:** favicon.svg — aa in Plex Mono.

**Style note**
Plex Sans for words, Plex Mono for anything that ran. Cream page, near-black text, one green for links. If the site is prettier than the gitviz calendar, strip it.

**Reuse block**

```
Fonts: IBM Plex Sans + IBM Plex Mono.
Colors: text #111111, background #F6F4EF, accent #215A4C, code ground #ECE8E1.
Mood: calm frame. No PaperMod defaults. No Notion menu. No gradient hero.
```

---

## Images

| Need     | Use                      | Not                |
| -------- | ------------------------ | ------------------ |
| gitviz   | real terminal calendar   | generated heatmap  |
| Euler    | real go test -bench=.    | generated code art |
| Task API | real Swagger             | generated UI       |
| Favicon  | aa svg                   | ornate logo        |
| Me       | GitHub avatar or nothing | generated portrait |

**Rejected:** PaperMod dark hero + Notion template links as the first thing a hiring manager sees. That upstages the Go CLI. Same for a generated glass terminal.

**Bench (real):**

```
goos: linux
goarch: amd64
pkg: project-euler/problem7
cpu: AMD Ryzen 7 7435HS
BenchmarkFindPrime-8 714 1686627 ns/op
PASS
ok      project-euler/problem7  1.210s
```
