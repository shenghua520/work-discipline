# Project notes | private experience for a specific backend

> Trigger: read only when operating **this particular backend**; do not apply these field semantics to other projects.
> This file holds "pitfalls of one system", not general discipline. General rules live in `execution-layer.md`.

## Reading configuration

- Read configuration with GET only; **never send an empty-body POST** — that backend treats it as a reset command and wipes the configuration.

## Bulk jobs

- Asynchronous responses look like `result:true` + `taskId`; **you must read back and record the result** — never treat "accepted" as "applied".

## Full review

- During a full scan, classify fields into two groups: **a STATIC change is a failure**, **VOLATILE gets reported only**. Judge "no more, no less" by specific ID existence, never by totals (totals drift).

## How to use

Treat these three as the "project adapter": the seven-step method in `execution-layer.md` is the skeleton, these are the concrete parameters. When switching to a different backend, keep the skeleton and discard these parameters — do not mistake them for cross-project rules.
