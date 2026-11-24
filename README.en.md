# work-discipline

Long-term collaboration discipline and behavioral guidelines. It turns "how to work with people" into a set of executable hard rules: list tasks before starting, scan skills, ask before installing missing capabilities, deliver only with evidence, confirm before high-risk actions, and apply a full methodology to write operations and delegation.

## Capabilities

- **Start-of-task alignment**: List goal + steps + status before every task. Do simple tasks directly; stop for confirmation on complex or high-risk ones.
- **Scan skills**: Load the 1–3 best-matching skills by description and explain why. For missing capabilities, search real candidates, ask once, and never install without approval.
- **Deliver with evidence**: Before/after comparison, tests, readback values, links. "I fixed it" does not count.
- **Hard boundaries**: Deletion, publishing, force-push, migration, external upload, reading secrets / user data — confirm first, then act. Never auto-execute remote write operations.
- **Execution layer (doing it right)**: Seven-step method for online changes and batch jobs — backup analysis → work-item table → minimal change → small-sample test → batch processing → three review rounds → retrospective. Every step must produce an artifact.
- **Delegation layer (delivering it right)**: Four timing phases when delegating to AI / teammates / automation — restate before starting, remove bottlenecks during execution, evidence-only at delivery, change the environment on error.
- **Self-maintenance**: New supersedes old, write as instructions, four-question write threshold, layer by scope.

## Triggers

- Call this skill before every task (relies on a standing hook in the user-level memory file).
- Triggered when the user says "follow the memory", "self-check", or "list tasks".
- On online write operations / batch jobs / delegation / memory edits, read the corresponding section below.

## Install and restore

1. **Directory**: Place this repository's `skills/work-discipline/SKILL.md` in your tool's skill installation directory to enable it.
2. **Cross-device**: Clone this repository and copy `skills/work-discipline/SKILL.md` to the path above.
3. **Standing hook**: Write a line in the user-level memory file: "call the work-discipline skill before every task". Rebuild it after switching machines if lost; otherwise triggering is probabilistic.

## Repository structure

```text
.
├── README.md                        # Chinese documentation
├── README.en.md                     # English documentation
└── skills/
    └── work-discipline/
        ├── SKILL.md                 # Rules body, Chinese (authoritative copy)
        └── SKILL.en.md              # Rules body, English translation
```

## Strengths

- **Turns implicit preferences into explicit rules**: Verbal habits become verifiable actions, reducing omissions from "going by impression".
- **Two layers interlock**: Execution layer manages "doing it right", delegation layer manages "delivering it right"; each rule marks its counterpart in the other layer, so they do not conflict.
- **Lean layering**: Standing layer holds only high-frequency hard rules + routing index; low-frequency chapters load on demand. Main file slimmed from 2821 to 1072 characters.
- **Field-tested**: Validated with two methods — a blind test of "does it output an action" and an independent-path readback after a real task. Not written off the cuff.

## Weaknesses / limitations

- **Enabled ≠ always invoked**: Skill loading is decided by the AI per task; a case was observed where "already read the rules so skipped the call" — behavior complied but the trigger mechanism did not run. A standing hook raises the probability but is not a hard guarantee.
- **Prompt layer, not a hard interceptor**: To make "never miss" absolute, use a Hook / script to block at the mechanism level; desktop clients may not support this.
- **Rules get diluted**: The longer the file, the more it gets skimmed; repeatedly writing "never do X" makes X more salient. Prune regularly.
- **Not for opinion tasks**: Writing is thinking. Such content must be written by the human; the skill only finds / organizes / verifies.

## Change log

- Rebuilt repository as Public, README rewritten in a standardized form; `skills/work-discipline/SKILL.md` keeps the full authoritative Chinese text.
- Historical lineage: added README → renamed workbuddy-memory → work-discipline → first commit uploading SKILL.md (old repository deleted, history not migrated).
- Added English counterparts: `README.en.md` and `skills/work-discipline/SKILL.en.md`.
