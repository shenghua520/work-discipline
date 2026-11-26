# Client compatibility matrix

The rules themselves are client-agnostic: plain imperatives, no brand names, no client-specific APIs. What binds this repo to a toolchain is the surrounding trio — **where to install, how to trigger, how to self-verify**. This table covers only those three.

**About the numbers**: token counts (≈1.6k / ≈3.4k) are **estimates derived from character counts**, not measurements from any client; actual usage depends on tokenizer and implementation — order of magnitude only. "10 rule files" is a hard fact, defined by `RULE_FILES` in `build_dist.py` and enforced by `--check`.

**Evidence level** (marked on every row; no blanks):

- `Verified locally` — checked on this repo's maintenance machine, reproducible.
- `Verified externally` — from a 2026-11-26 external review on a different machine; not reproduced locally, treat as "pending re-check".
- `Not verified` — filled in from common convention; **confirm before installing**, do not treat as established fact.

## Matrix

| Client / family | User-level skill dir | Resident-instruction location | On-demand file reads | Recommended build | Evidence |
|---|---|---|---|---|---|
| **WorkBuddy** | `~/.workbuddy/skills/` | Settings panel "Instructions to WorkBuddy" → `personalization.customPrompt` in `~/.workbuddy/app/app-config.json` (injected as `UserCustomPrompt`) | Yes (`Read` / `Skill` tools) | **Directory build**: copy the whole `work-discipline/` dir | Verified locally |
| **Claude / Anthropic family** | `~/.claude/skills/` | `CLAUDE.md` (user or project level) | Yes | **Directory build** + one trigger line in `CLAUDE.md` | Not verified (common convention) |
| **Doubao / Codex-like desktop** | `.user_skills` (user level); built-in `.skills` gets reconciled away by the client | Preferences / memory panel | Depends on implementation | **Directory build first**; use the `dist/` flat build if on-demand reads are unavailable | Verified externally (2026-11-26 review); not reproduced locally |
| **AGENTS.md family** (Cursor / Cline / Codex CLI, etc.) | No universal skill dir; typically a project-level `AGENTS.md` | Project-root `AGENTS.md` (user-level location varies) | Usually single-file only | **Flat build**: merge `dist/work-discipline.flat.md` into `AGENTS.md` | Not verified (common convention) |
| **rules family** (`.cursor/rules/`, `.github/copilot-instructions.md`, etc.) | The rules directory is the entry point; no separate skill dir | The corresponding rules file | Usually single-file only | **Flat build**: drop the flat file into the rules dir; wrap in the required `.mdc` / frontmatter format if needed | Not verified (common convention) |
| **Gemini CLI** | No universal skill dir | `GEMINI.md` | Depends on implementation | **Flat build** merged into `GEMINI.md` | Not verified (common convention) |

## Which build to use

1. **Directory build (default)**: `skills/work-discipline/` as a whole. Main file keeps high-frequency rules + routing; details load on demand. Pros: ~1.6k resident tokens. Cons: copying only `SKILL.md` fails silently. **Use only when the client can read files on demand.**
2. **Flat build (fallback)**: `dist/work-discipline.flat.md` (or `.flat.en.md`). Every rule inlined, no routing, no external dependency. Pros: one file is complete. Cons: resident tokens like the old single-file build (≈3.4k), and rule order is precedence. **Use when the client can only read one file.**
3. **English build**: every `*.en.md` is a translation of the same rule, not a second skill. Local installs only need the Chinese main file; the English build is for cross-language teams / external distribution.

## Client-agnostic resident instruction

```
Call the work-discipline skill before every task; the rules live in that skill, never rephrase them from memory.
```

**Write only two things: when to call, and where the rules are.** Never copy the rule body into it — two versions conflict, and a resident instruction that looks like the rules makes the agent assume they are loaded and skip the skill. For flat-build clients, change it to "read the discipline section of AGENTS.md before starting", and still do not excerpt rules.

## Self-verification without Python

`manifest.json` at the repo root lists SHA256 and byte count for every file. **Any language, any OS can verify with hashes alone**; Python is an optional enhancement:

```bash
# Linux / macOS / Git Bash
sha256sum skills/work-discipline/SKILL.md
# Windows PowerShell
Get-FileHash -Algorithm SHA256 skills\work-discipline\SKILL.md
```

The semantic self-check script `scripts/verify_skill.py` is **not part of the 10-file installed copy** — fetch it from the repo separately. Inside the repo use `python scripts/verify_skill.py`; to check an installed copy pass the manifest explicitly: `python <script> <install-dir> --manifest <manifest>`. `build_dist.py --check` (repo only) verifies flat builds and manifest against sources. Without Python or the script, use the manifest for hash self-verification (`sha256sum` / `Get-FileHash`) — fully offline.

## Unknown client? Answer three questions

The table is a snapshot and clients keep multiplying. For a new client, do not wait for the table — ask on site:

1. **Can it read files on demand?** Yes → directory build. Only one file (AGENTS.md / a rules file) → `dist/` flat build. **This one matters most; getting it wrong turns discipline into an error generator.**
2. **Where is its user-level skill dir?** Look for a user-level "skills / global rules" directory. If there is one, install there; otherwise fall back to a project-level dir or the flat build. When unsure, check official docs — do not guess.
3. **Where does the resident instruction go?** Find the client's "custom instructions / preferences / CLAUDE.md / AGENTS.md / GEMINI.md" entry and write one trigger line, never the rule body. If you cannot find one, just say "call the work-discipline skill" at kickoff manually — do not edit config files just to force a trigger.

Answer all three before installing; if you cannot answer #1, do not install the directory build.

## One hard boundary

**"Stop if references cannot be read" is a directory-build clause.** The flat build overrides it in the file header — a flat build has no `references/` by definition, and following that clause literally would produce one error per task, worse than no install at all. Installing the directory build into a client that cannot read files on demand turns discipline into an error generator; check that column before installing.
