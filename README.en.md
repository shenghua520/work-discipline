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
           ├── memory-maintenance.en.md
           ├── project-notes.md
           └── project-notes.en.md
   ```

   ⚠️ **Copying `SKILL.md` alone breaks it**: the main file states that online writes, bulk jobs, and delegation require reading the matching `references/` file first. Without those files the execution-layer and delegation-layer rules fail as a whole — and they fail **silently**, because the skill still loads and the rules are simply skipped. Always bring the whole directory.

2. **Resident hook (a trigger, not a copy of the rules)**: put one line in the client's resident-instruction setting — "call the work-discipline skill before every task; the rules live in that skill". The location depends on the client — in WorkBuddy it is the "Instructions to WorkBuddy" panel in settings (stored locally as `personalization.customPrompt` in `~/.workbuddy/app/app-config.json`).

   ⚠️ **Never copy the rule body into it**. Two versions of the same rule conflict, and conflicting rules get picked at random; subtler still, a resident instruction that looks like the rules makes the agent assume the rules are already loaded and **skip invoking the skill** — worse than having no hook at all.

3. **Cross-device recovery (git first)**: `git clone https://github.com/shenghua520/work-discipline.git`, then overwrite the whole `skills/work-discipline/` directory into the local skills directory. If the pull fails, keep using the existing local copy — never let it block the work.
4. **Recovery without git** (verified usable when git is not on PATH, ordered by feasibility):

   - **zip / tarball**: repo home → `Code` → `Download ZIP`; extract and copy the whole `skills/work-discipline/` dir into the user-level skills directory.
   - **Per-file raw download (bash)**:

     ```bash
     BASE="https://raw.githubusercontent.com/shenghua520/work-discipline/main/skills/work-discipline"
     DEST="$HOME/.claude/skills/work-discipline"   # adjust for your client
     for f in SKILL.md SKILL.en.md \
       references/execution-layer.md references/execution-layer.en.md \
       references/delegation-layer.md references/delegation-layer.en.md \
       references/memory-maintenance.md references/memory-maintenance.en.md \
       references/project-notes.md references/project-notes.en.md; do
       mkdir -p "$DEST/$(dirname "$f")"
       curl -fsSL "$BASE/$f" -o "$DEST/$f" || echo "FAILED: $f"
     done
     # the manifest lives at the repo root, not inside skills/ — fetch it separately
     curl -fsSL "https://raw.githubusercontent.com/shenghua520/work-discipline/main/manifest.json" \
       -o "$DEST/manifest.json" || echo "FAILED: manifest.json"
     ```

   - **Per-file raw download (PowerShell)**:

     ```powershell
     $base = "https://raw.githubusercontent.com/shenghua520/work-discipline/main/skills/work-discipline"
     $dest = "$env:USERPROFILE\.workbuddy\skills\work-discipline"  # adjust for your client
     $files = @("SKILL.md","SKILL.en.md",
       "references/execution-layer.md","references/execution-layer.en.md",
       "references/delegation-layer.md","references/delegation-layer.en.md",
       "references/memory-maintenance.md","references/memory-maintenance.en.md",
       "references/project-notes.md","references/project-notes.en.md")
     foreach ($f in $files) {
       $out = Join-Path $dest ($f -replace '/', '\')
       New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
       Invoke-WebRequest -Uri "$base/$f" -OutFile $out
     }
     # the manifest lives at the repo root — fetch it separately
     Invoke-WebRequest -Uri "https://raw.githubusercontent.com/shenghua520/work-discipline/main/manifest.json" -OutFile (Join-Path $dest "manifest.json")
     ```

   Verify with `manifest.json` SHA256 sums (below) — do not just check that files exist. To self-check an installed copy you must pass the manifest explicitly; otherwise the script refuses to present the repo's own manifest as a check of your directory:

   ```bash
   python scripts/verify_skill.py "$DEST" --manifest "$DEST/manifest.json"
   ```

5. **Switching clients**: skill dirs, resident-instruction locations, and on-demand read support differ per client. Before installing, see the matrix in `docs/clients.md` (Chinese) / `docs/clients.en.md` (English) — every row carries an evidence level (verified locally / verified externally / not verified). **Clients that can only read a single file must use the `dist/` flat build, not the directory build.**

## Repository layout

```text
.
├── .github/workflows/verify.yml     # CI: dual job (with/without PyYAML) × dual OS
├── LICENSE                          # MIT
├── README.md                        # this document (Chinese)
├── README.en.md                     # this document (English)
├── docs/
│   ├── clients.md                   # client compatibility matrix (Chinese, evidence levels)
│   └── clients.en.md                # client compatibility matrix (English)
├── dist/
│   ├── work-discipline.flat.md      # flat build (no references; for single-file clients)
│   └── work-discipline.flat.en.md
├── manifest.json                    # SHA256 + byte count for every file (no Python needed)
├── scripts/
│   ├── verify_skill.py              # semantic self-check: frontmatter + alignment + routes
│   └── build_dist.py                # build / verify flat builds and manifest
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
python scripts/verify_skill.py              # repo self-check (auto manifest only when target is inside the repo)
python scripts/verify_skill.py <install-dir> --manifest <manifest-path>   # installed copy: explicit manifest required
python scripts/build_dist.py --check        # are flat builds and manifest in sync with sources?
```

`verify_skill.py` checks strict YAML parsing of frontmatter, description length, CN/EN structural fingerprints (items / headings / bold pairs / table rows / code fences / backticks), bidirectional route closure, absence of brand names, and that the masking rule no longer exposes the first 4 characters. `build_dist.py --check` verifies that the `dist/` flat builds and `manifest.json` match the sources — so editing a rule without regenerating the distribution is caught. Neither script uses the network or writes files.

**Exit codes**: `0` = fully verified; `1` = a FAIL; `2` = a PARTIAL (e.g. PyYAML missing, syntax not verified) — PARTIAL no longer masquerades as "all passed".

**CI covers both branches**: `verify-full` (ubuntu + windows, PyYAML installed, asserts `exit=0`) + `verify-no-deps` (`python -S`, asserts `exit=2` and a `PARTIAL` marker). Previously CI only installed PyYAML, so the PARTIAL branch was never exercised — now it is asserted directly.

**Self-verification without Python**: `manifest.json` lists SHA256 and byte count for every file, checkable in any language (`sha256sum` / PowerShell `Get-FileHash`). Python drops from "required" to "optional enhancement".

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

- **v6 verification-loop fix**: fixed "installed copy passes self-check falsely" — section 6 previously used the repo's own manifest to hash the repo's own files, unrelated to the target directory passed in. Now the repo manifest is auto-used only when the target is inside the repo layout; checking any installed copy requires explicit `--manifest`, otherwise it is marked PARTIAL (exit 2) instead of claiming a false green. Hash comparison is based on the target directory, covering only its 10 rule files. CI gained a negative-test job (deliberately pollutes an installed copy and asserts failure). README install tree gained both project-notes files, recovery loops fetch `manifest.json`, terminology unified to "client resident instruction", an unknown-client decision flow was added, and the flat build dropped a duplicate separator.
- **v5 distribution-layer rework**: added `docs/clients.md` compatibility matrix (every row tagged verified-locally / verified-externally / not-verified); added `dist/` flat builds + `manifest.json` (SHA256 verifiable without Python), generated and checked by `scripts/build_dist.py --check`; CI split into dual jobs (with/without PyYAML) × dual OS, covering the previously untested PARTIAL branch; installation docs gained zip and per-file raw recovery recipes (bash + PowerShell); the hard reference to a "resident hook file" became "client resident instruction (also re-read if the client persists it as a file)", and the flat build header overrides directory-only clauses so single-file clients do not trip the "stop if references cannot be read" rule.
- **v4 second-review fixes**: added `project-notes` to the main routing table (index closure); self-check upgraded — missing PyYAML now yields PARTIAL with distinct exit codes `0/1/2` instead of a silent SKIP followed by "all passed", CN/EN alignment upgraded from item counts to structural fingerprints (which immediately caught a 6-vs-8 backtick drift in project-notes), and route checks now work in both directions; added `.github/workflows/verify.yml` CI gate; delegation layer notes which clauses apply in a single-person/single-agent setup, and memory maintenance notes the boundary against client-side preference/memory tools.
- **v3 external review fixes**: both descriptions converted to `>-` block scalars (fixes strict-YAML failure in the English frontmatter); masking tightened from first-4+last-4 to last-4 only; API replay clause gained three preconditions and an explicit ban on bypassing managed-network policy; backend-specific details (`empty-body POST` / `STATIC·VOLATILE` / `result:true+taskId`) moved into `references/project-notes.md`, leaving only portable rules in the execution layer; MIT LICENSE and `scripts/verify_skill.py` added.
- **v2 structural rework**: the main file keeps only high-frequency hard rules (≈55 lines); the execution layer, delegation layer, and memory maintenance move into `references/`, and the routing index becomes real; two new rules added — "never echo credentials" and "re-read after compaction or instance switch"; duplicate items merged (task list vs work items; sweeping skills vs asking before adding capabilities) to remove self-contradiction; environment facts moved out of the rule body into this document.
- **v1**: added README → renamed from workbuddy-memory to work-discipline → first created and uploaded SKILL.md.
