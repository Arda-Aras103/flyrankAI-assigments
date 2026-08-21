# Frame it as cases

**Voice card:** direct, plain, specific, short, explanatory, no buzzwords

**Audience:** a hiring manager looking for a junior DevOps, cloud, or software engineer  
**One action:** review the CV and consider an interview

---

## Home

CS student. Go, Linux, and small tools I actually run. I want a junior DevOps, cloud, or engineering interview.

The CV can list Go. These pages show a repo you can clone and a small API you can start.

**Do this:** email me and I will send the CV.

---

## Projects

### Project Euler

Repo: https://github.com/Arda-Aras103/project-euler

**The problem.** I wanted to show I can write Go and think through algorithms, not just list the language on a CV. I started at problem 1 and went in order.

**What I did.** I solved the first 10 in Go. Each problem has its own folder. I kept dependencies at zero. I wrote every solution myself. I added tests and benchmarks from problem 4 on, including Go’s newer `b.Loop()` style. When a first version was correct but slow, I sped most of them up. A few I left, because the next step was a heavy closed-form I did not want to pretend I had derived. Helper: `new-problem.sh`. Run: `go run ./problem10`. Bench: `go test ./problem10 -bench=.`

**What came of it.** The first 10 are done and the repo runs without setup. Benchmarks were worth it; they showed which rewrite actually helped. A hiring manager can clone it and run a problem in a few minutes. This shows Go plus algorithmic work. It is not yet a workflow CLI. Next time I would test from problem 1, add a short note per problem, keep going in order, and commit the slow version before the fix.

### Task API (internship, BE-01)

Repo: https://github.com/Arda-Aras103/flyrankAI-assigments/tree/main/BE-01

**The problem.** The assignment asked for a Task API. I did not want a database or an extra server in the way, so I kept the data in memory.

**What I did.** I wrote an in-memory CRUD API with FastAPI. It started as one model. Create got messy, so I split it into create, update, and the full Task. New ids are last id + 1, or 1 if the list is empty. Missing task → 404. Empty or invalid body → 400. I overrode the framework’s default status codes and forced 400. I checked it with curl. Swagger is at `/docs`.

**What came of it.** It runs locally. Someone else can start it with `uvicorn` and try the endpoints. This does not prove I can build Go CLIs. It proves I can ship a small HTTP service you drive from the command line. Next time I would write it in Go and add persistent storage.

---

## About

CS student (Ege University, class of 2028). I care about Go, Linux, and tools I can compile, test, and run myself.

I am proving I can turn that into working software, not a skill list. Start with the Project Euler repo. The internship Task API is the other piece: a small service with clear status codes and a README.

---

## Contact

**One action:** email me and I will send the CV.

- GitHub: https://github.com/Arda-Aras103
- Project Euler: https://github.com/Arda-Aras103/project-euler
- Internship repo: https://github.com/Arda-Aras103/flyrankAI-assigments
- LinkedIn: https://www.linkedin.com/in/arda-aras-cavdur/
- Email: cavduraras103@gmail.com

---

## Before / after

**Generic AI line**

> I am a results-driven Computer Science student passionate about leveraging Go and modern backend frameworks to deliver high-quality, scalable solutions and impactful algorithmic thinking.

**Edited**

> CS student. Go, Linux, and small tools I actually run. I want a junior DevOps, cloud, or engineering interview.
