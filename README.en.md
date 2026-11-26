# work-discipline

Long-term collaboration discipline and behavioral guidelines. It turns "how to work with people" into a set of executable hard rules: restate and clarify before starting, search skills online and weigh them, look things up when blocked, attach evidence when handing off, confirm high-risk actions; online changes and delegation each get a complete methodology.

Chinese and English versions, rule by rule.

## Capabilities

- **Restate, clarify, then confirm**: restate the goal and problem in your own words, break out the work items, and turn the user's wording into an explicit task definition for confirmation before acting; for simple tasks, restate and go — do not stall for process.
- **Sweep skills and MCPs**: search online for real candidates (not only what is installed), judged on four weights — task fit, environment compatibility, maintenance activity, and introduction cost; ask before adding capabilities, never install silently.
- **Look things up when blocked**: when paths, APIs, or error messages stop you, check official docs and community solutions first; never guess from memory.
- **Attach evidence when handing off**: before/after comparison / test / read-back value / link; "I fixed it" does not count.
- **Hard boundaries**: deletion, publishing, force-push, migration, external upload, and reading keys or user data are confirmed first; credentials appear only in masked form in any output.
- **Execution layer (doing it right)**: the seven-step method for online changes and bulk jobs — back up and analyze → list work items → minimal change → small-sample test → bulk run → three review rounds → retrospective, with an artifact required at every step.
- **Delegation layer (delivering it right)**: four moments when delegating to AI, teammates, or automations — restate before starting, remove your dependency while running, accept only evidence at handoff, fix the environment when it goes wrong.

## Triggering

- Call this skill before every task (depends on the resident hook in the user-level memory file).
- Triggered when the user says "follow the memory", "self-check", "list tasks", "confirm before starting", or any task kickoff.
- When online writes / bulk jobs / delegation / memory edits come into scope, the main file routes to the matching file under `references/` — **this is a hard requirement: if the file cannot be read, stop and report the error; never reconstruct the details from memory**.

## Installation and recovery

**The unit of installation is a directory, not a file.** One skill = one directory; `SKILL.md` inside it is the only entry point, and everything else is a companion resource that travels with it.

1. **Copy the whole directory**: put `skills/work-discipline/` into the user-level skills directory (common shapes: `~/.workbuddy/skills/`, `~/.claude/skills/`), ending up as:

   ```text
   <user-level skills dir>/
   └── work-discipline/
       ├── SKILL.md
       ├── SKILL.en.md
       └── references/
           ├── execution-layer.md
           ├── execution-layer.en.md
           ├── delegation-layer.md
           ├── delegation-layer.en.md
           ├── memory-maintenance.md
           └── memory-maintenance.en.md
   ```

   ⚠️ **Copying `SKILL.md` alone breaks it**: the main file states that online writes, bulk jobs, and delegation require reading the matching `references/` file first. Without those files the execution-layer and delegation-layer rules fail as a whole — and they fail **silently**, because the skill still loads and the rules are simply skipped. Always bring the whole directory.

2. **Resident hook (a trigger, not a copy of the rules)**: put one line in the client's resident-instruction setting — "call the work-discipline skill before every task; the rules live in that skill". The location depends on the client — in WorkBuddy it is the "Instructions to WorkBuddy" panel in settings (stored locally as `personalization.customPrompt` in `~/.workbuddy/app/app-config.json`).

   ⚠️ **Never copy the rule body into it**. Two versions of the same rule conflict, and conflicting rules get picked at random; subtler still, a resident instruction that looks like the rules makes the agent assume the rules are already loaded and **skip invoking the skill** — worse than having no hook at all.

3. **Cross-device recovery**: `git clone https://github.com/shenghua520/work-discipline.git`, then overwrite the whole `skills/work-discipline/` directory into the local skills directory. If the pull fails, keep using the existing local copy — never let it block the work.

## Repository layout

```text
.
├── LICENSE                          # MIT
├── README.md                        # this document (Chinese)
├── README.en.md                     # this document (English)
├── scripts/
│   └── verify_skill.py              # self-check: frontmatter + CN/EN alignment + routes
└── skills/
    └── work-discipline/
        ├── SKILL.md                 # main rule file · Chinese · sole entry point
        ├── SKILL.en.md              # main rule file · English
        └── references/
            ├── execution-layer.md      # seven-step method + three iron rules
            ├── execution-layer.en.md
            ├── delegation-layer.md     # four moments of delegation
            ├── delegation-layer.en.md
            ├── memory-maintenance.md   # memory maintenance rules
            ├── memory-maintenance.en.md
            ├── project-notes.md        # private experience for one backend (void elsewhere)
            └── project-notes.en.md
```

## Self-check

```bash
python scripts/verify_skill.py
```

Checks strict YAML parsing of frontmatter (only when PyYAML is installed), description length, CN/EN item alignment, existence of routed files, absence of brand names, and that the masking rule no longer exposes the first 4 characters. Prints md5 of every file for remote comparison. No network, no writes, exit code 0 = all passed.

## Design trade-off: why references

| Approach | Resident tokens | If files are missing | Choice here |
| --- | --- | --- | --- |
| One file with everything | ≈3400 | n/a | ✗ low-frequency rules get skimmed |
| Split into references | ≈1600 (main file) | silent failure — now guarded | ✓ |
| Three separate skills | may all load at every kickoff | installed separately, easy to miss one | ✗ defeats "one skill, one workflow" |

The reason for splitting: low-frequency details (the delegation layer was 25% of the file and is highly personal) should not enter context on every kickoff; and a hard clause — "stop and report when the file cannot be read" — turns "missing file = silent degradation" into a visible error.

## Advantages

- **Turns implicit preferences into explicit rules**: spoken habits become verifiable actions, reducing the "went from memory" kind of omission.
- **Two interlocking layers**: the execution layer handles "doing it right", the delegation layer handles "delivering it right"; each rule points at its counterpart, so they do not fight.
- **Load on demand**: the resident part keeps only high-frequency hard rules plus a routing index; low-frequency details load only when triggered.
- **Tested**: validated with two probes — "blind test whether an action gets produced" and "read back through an independent path after a real task" — not written on intuition.

## Limitations

- **Enabled ≠ called every time**: skills load on demand based on the AI's own judgment, and a real case was observed where the AI read the rules and then skipped calling the skill — compliant behavior, but the trigger mechanism never ran. The resident hook raises the probability; it is not a hard guarantee.
- **Prompt layer, not hard enforcement**: guaranteeing "this can never be missed" requires hooks or scripts, and desktop clients may not support that.
- **The cost of splitting**: installation must copy a whole directory; copying a single file fails silently. A "stop and report when unreadable" clause guards it, but the installation bar genuinely rises.
- **Rules dilute**: the longer the file, the more likely it is skimmed; repeatedly writing "never do X" makes X more salient, so periodic trimming is needed.
- **Not for opinion work**: writing is thinking — posts, articles, and judgments stay human-written; the skill only finds, organizes, and verifies.

## Known environment constraints

These are states of a particular machine / repository, **not rules**, so they stay out of the `SKILL.md` body:

- The GitHub MCP write endpoint returns `403 Resource not accessible by integration` (the OAuth scope lacks `repo`); the read endpoint works — writes to that repository go through `git push`.
- The machine's global git identity is a placeholder (`Your Name` / `your.email@example.com`); set `git config user.name` / `user.email` per repository before committing, or commits cannot be attributed.

## Changelog

- **v3 external review fixes**: both descriptions converted to `>-` block scalars (fixes strict-YAML failure in the English frontmatter); masking tightened from first-4+last-4 to last-4 only; API replay clause gained three preconditions and an explicit ban on bypassing managed-network policy; backend-specific details (`empty-body POST` / `STATIC·VOLATILE` / `result:true+taskId`) moved into `references/project-notes.md`, leaving only portable rules in the execution layer; MIT LICENSE and `scripts/verify_skill.py` added.
- **v2 structural rework**: the main file keeps only high-frequency hard rules (≈55 lines); the execution layer, delegation layer, and memory maintenance move into `references/`, and the routing index becomes real; two new rules added — "never echo credentials" and "re-read after compaction or instance switch"; duplicate items merged (task list vs work items; sweeping skills vs asking before adding capabilities) to remove self-contradiction; environment facts moved out of the rule body into this document.
- **v1**: added README → renamed from workbuddy-memory to work-discipline → first created and uploaded SKILL.md.
