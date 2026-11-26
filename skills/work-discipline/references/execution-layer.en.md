# Execution layer | online changes and bulk jobs

> Trigger: online writes, bulk jobs, and commit / publish / migrate / delete actions.
> Steps run in order, cannot be skipped or merged; every step must produce an artifact — no artifact means it did not happen.

## Seven steps

1. **Back up and analyze**: before any write, take a read-only full snapshot (timestamped, covering every sub-tab of the module, not only the named item) plus a baseline table (row count / ID range / field distribution). Before reading configuration, confirm the system's safe read method — some backends treat an empty-body POST as a reset command; such project-specific details live in `project-notes.en.md`.
2. **List work items**: a plan table — object / current state / target / basis / risk / acceptance, one verifiable unit per row; "basis" must never be empty; anything you cannot think through goes in a separate "to confirm" list, never smuggled into the plan.
3. **Minimal change**: touch only the named scope and fields; write back the fields you mean to change explicitly (never expand with `...old snapshot`); freeze the "allowed change list" first, and at acceptance there must be zero changes outside it. Problems found outside the scope — report, do not act.
4. **Small-sample test**: change one (at most a very small batch) → read back → three checks (target changed / side effects not clobbered / non-targets untouched) → auto-rollback. Pick boundary samples, never convenient ones; if it fails, go back and fix the design — never "try a few more and see".
5. **Bulk runs**: batch ≤50 (conservatively 20–30), sleep between batches, log each batch, abort immediately when failures exceed the threshold; asynchronous jobs must be read back and accounted for — never treat "accepted" as "applied". Response field names vary by system; see `project-notes.en.md`.
6. **Multiple reviews**: at least three rounds with different angles — sample level (pull 3–5 and judge plausibility) / full level (scan with no filter, distinguish which fields are failures if changed and which are report-only — classification lives in `project-notes.en.md`) / attribution level (time window + primary key range + specific ID existence, three-way cross-check); plus one independent path (spin up a separate read-only script and re-read after a fresh login; never reuse the writing script's result).
7. **Summarize lessons**: work-item ledger + failure retrospective (symptom → root cause → fix → how to prevent next time) + write back to the experience library (per that file's own gate).

## Three iron rules

- When blocked, gather evidence — never guess (API names, popup locations, failure causes: the number-one cause of every timeout so far).
- Trust read-back values from the backend API, not the front-end page (it caches); to judge "no more, no less" use specific ID existence, never totals (they drift).
- A correction is itself a write — it goes through small-sample plus read-back too; never fix in bulk directly.

## Writing files and committing

- **Prefer version control for file writes**: edit locally and then `add` / `commit` / `push`; do not paste file contents into a web form character by character — pasting drops line breaks and breaks YAML frontmatter. If you must edit on the web, read the first line and indentation back afterwards to verify.
- **Confirm the git identity is not a placeholder before committing**: if `git config user.name` / `user.email` still hold defaults like `Your Name` / `your.email@example.com`, set them per repository first — a placeholder identity makes commits unattributable.
- **Verify byte-for-byte after pushing**: compare hashes between the remote and the local source file (e.g. align `git show origin/main:<path>` with the local `md5sum`); "the push command did not error" is not accepted as evidence of success.
- **No secrets in the repository**: before writing, confirm the file holds no tokens, `.env`, or real user data; record any leaked credential in masked form only, and never echo the full value in commit messages or logs.
