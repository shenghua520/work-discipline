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
- **Draw a boundary against the client's preference / memory tools**: built-in preferences, memory, and personalization are a separate source from this skill's memory layer — never write the same rule into both. The resident instruction holds only "when to call which skill", rules live only in this skill, and client-side tools hold only their own preferences. If the same rule appears in both, delete the resident-instruction copy immediately and treat the skill body as authoritative (conflicting rules get picked at random).

## Keeping it fresh

- Separate environment facts from rules: **rules** belong in the body (the AI can act on them); **environment state** (one repository's 403, one machine's default config) belongs in the README or notes — an AI reading environment facts has no executable action.
- **The resident instruction is a trigger, not a copy of the rules**: the client's resident instruction (custom instruction / customPrompt) states only *when to invoke which skill* — never copy the rule body into it. Two failures to avoid: ① after the rules change the resident instruction is not updated, leaving two conflicting versions of the same rule — and conflicting rules get picked at random; ② the resident instruction looks like the rules, so the agent assumes the rules are already loaded and skips invoking the skill. Correct shape: one trigger line plus "the rules live in the skill".
- Keep the client resident instruction on its own: in the client's instruction setting, keep only one trigger line (e.g. "call the xxx skill before every task"); the rule body is not repeated there — duplication is conflict risk. If the client persists that instruction as a separate file, re-read it together with the skill.
- Read back and verify after every change: the frontmatter's first line and field line breaks, item counts, one-to-one correspondence between Chinese and English items, and matching hashes between remote and local.
