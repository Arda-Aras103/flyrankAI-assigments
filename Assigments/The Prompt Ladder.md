# The Prompt Ladder

Track: General AI Fluency / backend
What actually happened: I wanted a custom status code on bad input. The model kept pushing FastAPI's default (422) instead.
Voice: direct, plain, specific, short, explanatory, no buzzwords

---

## Baseline (weak)

**Prompt**

```
I'm stuck, help me.
```

**Output (excerpt)**

> FastAPI already handles this. Leave the default validation in place. 422 Unprocessable Entity is the correct status for a bad body. You do not need to set a status code yourself.

**Notes**

- Changed in the prompt: nothing.
- Improved in the output: nothing to compare.
- Still failed: it never asked which status I wanted. It defended the default.
- Try next: name the task.

**Layer:** clearer goal

---

## Version 1 — clearer goal

**Prompt**

```
I'm stuck on the Task API status codes. Help me finish the FastAPI CRUD.
```

**Output (excerpt)**

> For a FastAPI CRUD, use HTTPException and let Pydantic validate the body. Invalid JSON or a missing field should stay 422. That is the framework default and what OpenAPI expects.

**Notes**

- Changed in the prompt: named the stuck area (status codes / Task API).
- Improved in the output: it talked about this API instead of a random lecture.
- Still failed: it still chose 422 for me.
- Try next: I told it to "do it properly." That usually means more default.

**Layer:** quality criteria

---

## Version 2 — quality criteria (this one got worse)

**Prompt**

```
I'm stuck on the Task API status codes. Help me finish the FastAPI CRUD.
Follow FastAPI best practices and do it the proper way.
```

**Output (excerpt)**

> Best practice is not to override status codes. Keep 422 for validation errors so Swagger, clients, and FastAPI stay consistent. Custom 400/402 responses are against the framework.

**Notes**

- Changed in the prompt: "best practices / proper way."
- Improved in the output: nothing. It got more sure that the default was right.
- Still failed / worse: the stuck point was "I do not want the default." This prompt made the model defend the default harder.
- Try next: say the code I want and forbid the default.

**Layer:** real context

---

## Version 3 — real context

**Prompt**

```
I'm stuck on the Task API status codes. Help me finish the FastAPI CRUD.

Context: FlyRank BE-01. In-memory only.
I do not want the FastAPI default 422.
Bad / empty body must be 400. Missing id must be 404. Delete success must be 204.
I first said 402; that was the wrong code. Use 400.
Do not talk me into keeping 422.
```

**Output (excerpt)**

> 422 is Pydantic running before your handler. 402 is Payment Required — do not use it.
>
> Accept title as optional, then if it is missing or blank return JSONResponse(status_code=400).
> Unknown id → 404. Delete → 204.
> Do not leave the default 422 on these paths.

**Notes**

- Changed in the prompt: the real rule (400 not 422), and that 402 was my mix-up.
- Improved in the output: it stopped selling 422. It named why 422 appears.
- Still failed: the fix is a paragraph. I still have to extract the change.
- Try next: lock the answer shape.

**Layer:** specified output format

---

## Version 4 — specified output format

**Prompt**

```
I'm stuck on the Task API status codes. Help me finish the FastAPI CRUD.

Context: FlyRank BE-01. In-memory only.
I do not want the FastAPI default 422.
Bad / empty body must be 400. Missing id must be 404. Delete success must be 204.
I first said 402; that was the wrong code. Use 400.
Do not talk me into keeping 422.

Output exactly:
1. Why I get 422 (4 lines max)
2. Why not 402
3. The smallest code change for 400 / 404 / 204
4. Three curls
5. Nothing else
```

**Output (excerpt)**

> 1. Pydantic validates first, so a bad body never reaches your if. FastAPI returns 422.
> 2. 402 means payment required. This is a bad request, so 400.
> 3. Optional title + JSONResponse(400) on blank/missing; 404 if id missing; 204 on delete.
> 4. POST {}; GET /tasks/999; DELETE /tasks/1

**Notes**

- Changed in the prompt: five-part answer, then stop.
- Improved in the output: 422 vs 400 vs 402 is visible in one screen.
- Still failed: it can still sneak 422 back in as a "also keep default for this case."
- Try next: force a check against the default.

**Layer:** verification requirements

---

## Version 5 — verification requirements

**Prompt**

```
I'm stuck on the Task API status codes. Help me finish the FastAPI CRUD.

Context: FlyRank BE-01. In-memory only.
I do not want the FastAPI default 422.
Bad / empty body must be 400. Missing id must be 404. Delete success must be 204.
I first said 402; that was the wrong code. Use 400.
Do not talk me into keeping 422.

Output exactly:
1. Why I get 422 (4 lines max)
2. Why not 402
3. The smallest code change for 400 / 404 / 204
4. Three curls
5. Nothing else

Before you finish, check:
- Empty/invalid body is 400, not 422 and not 402
- You did not tell me to keep the FastAPI default
- You did not add a database or another framework
If a check fails, delete that part and answer again.
```

**Output (excerpt)**

> Same four facts as v4.
> Checks: 400 not 422/402; default not recommended; no extra stack.

**Notes**

- Changed in the prompt: a check that the default did not sneak back.
- Improved in the output: the model has to reject 422 and 402 before stopping.
- Still failed: the check is still the model grading itself. I still run the curls.
- Try next: stop. This is the reusable prompt.

---

## Final reusable prompt

```
I'm stuck on {assignment}. The problem is {one behavior}.

Context:
- I want: {the status or result I want}
- I do not want the default: {what the tool does now}
- Do not talk me into the default.

Output exactly:
1. Why the default happens (4 lines max)
2. The smallest change
3. How I prove it
4. Nothing else

Before you finish, check:
- The answer uses my status/result, not the default
- You did not add extras I did not ask for
If a check fails, delete that part and answer again.
```

Filled for BE-01:

```
I'm stuck on FlyRank BE-01. The problem is FastAPI returns 422 on a bad body.

Context:
- I want: 400 on empty/invalid body, 404 on missing id, 204 on delete
- I do not want the default: 422
- Do not talk me into the default.
- 402 is the wrong code; do not use it.

Output exactly:
1. Why the default happens (4 lines max)
2. The smallest change
3. How I prove it (curl)
4. Nothing else

Before you finish, check:
- Empty/invalid body is 400, not 422 and not 402
- You did not tell me to keep the FastAPI default
- You did not add extras I did not ask for
If a check fails, delete that part and answer again.
```

---

## Side-by-side

| Version | Layer            | What the output did                      |
| ------- | ---------------- | ---------------------------------------- |
| 0       | none             | "Keep the default 422"                   |
| 1       | clearer goal     | Still 422, now with FastAPI jargon       |
| 2       | quality criteria | Worse. "Best practice = do not override" |
| 3       | real context     | 400, and 402 called wrong                |
| 4       | output format    | Why 422, why not 402, patch, curls       |
| 5       | verification     | Must not sell 422 again                  |

Earned its place: real context (400, not 422, not 402).
Did not help: quality criteria ("best practices / proper way").
