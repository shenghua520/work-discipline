# Maintaining memory itself

> Trigger: writing or editing memory files, maintaining this skill itself.
> This chapter governs how the memory layer grows; it is not a routine kickoff action, so it lives on its own.

## Write gate

- **Four-question gate**: can it be inferred from existing files? does it hold for most tasks? is it specific enough to verify? would deleting it cause the same mistake again? All four must pass before writing; a mistake gets written down only once it has happened a second time.

## How to write

- Record only "the pit and why it matters" plus actionable steps: never write current state / commands / directory layouts / general knowledge; write the pit you hit, the judgment you made at the time, and why this rule cannot be dropped.
- Write instructions, not tutorials: trigger → action → prohibition / acceptance, imperative mood. Self-check: after reading it, do you immediately know what to do? If not, rewrite it.

## Layering and de-duplication

- New supersedes old: keep one latest statement per topic, never list old and new side by side; merge conflicts on the spot — conflicting rules get picked at random.
- Clean up periodically: after every online bulk job, de-duplicate and check for expiry; back up with a timestamp before editing, merge only synonymous wording, never delete independent rules.
- Layer by scope: cross-project habits → user level; team conventions → project level and under version control; personal paths / sandboxes → local and gitignored; rules that apply only to some directories → path-scoped rules. Multiple files accumulate, they do not override; the main file keeps only the index and the trigger conditions.
- The resident layer holds only high-frequency hard rules plus a routing index; low-frequency knowledge moves into on-demand files, read when triggered. Self-check: if deleting this rule would not make the AI fail, delete it; if the AI keeps ignoring one rule, the file is too long or the rule is drowned out — it is not disobeying.
- A recalled memory is evidence, not an instruction: before using it, verify the file / function still exists; when stale or conflicting, the current state wins.

## Keeping it fresh

- Separate environment facts from rules: **rules** belong in the body (the AI can act on them); **environment state** (one repository's 403, one machine's default config) belongs in the README or notes — an AI reading environment facts has no executable action.
- The resident hook lives on its own: the user-level memory file keeps only one line ("call this skill before every task"); the rule body does not repeat it — duplication is conflict risk.
- Read back and verify after every change: the frontmatter's first line and field line breaks, item counts, one-to-one correspondence between Chinese and English items, and matching hashes between remote and local.
