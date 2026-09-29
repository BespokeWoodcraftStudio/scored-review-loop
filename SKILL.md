---
name: scored-review-loop
description: Use when reviewing, auditing or QA-ing finished build work, before merging a lane or branch, when running or designing a review loop, when deciding which model reviews or audits, or when a review returns findings and you need to know what blocks and what happens next. Carries the desk model (each desk scores 0 to 100 against the owner's bar words), the severities, the pass rule, the loop flow, the default models, the cost rules and a ready workflow script.
---

# Scored review loop

Work is judged by desks. A desk is one narrow reviewer with one lens. Each desk scores the work 0 to 100 against the owner's bar words. A cheap first pass reads everything; the strong model audits only the desks that are already at the bar.

## What a desk is

| Part | Meaning |
|---|---|
| Lens | The one thing this desk judges (correctness, look, wording, security, access, the target user, rules the repo must obey) |
| First pass | A role on the work model. Finds everything real, scores, says pass or fail |
| Final audit | A role on the audit model. Runs only if the first pass is at the bar. Confirms, downgrades, drops or adds findings, then scores |
| Scope | Its own desk only. Nobody signs off on another desk's lens |

## The score

- 0 to 100 per desk, against the bar words. Default words: functional, professional, premium, clean, easy to use. Set your own in the settings file.
- Default bar: 90. The bar is per desk, not an average.
- Score honestly. A pass sends the desk to the audit; a fail sends findings straight to the fixers.

## Severities

| Severity | Meaning | Blocks a pass |
|---|---|---|
| blocking | A real person or run hits it and the work is unusable or unsafe | yes |
| major | Real harm in a plausible case | yes |
| minor | Rough edge a real person could hit | no, but fixers still fix it and it keeps scores down |
| note | Preference, or a case nobody meets | no |

A finding needs three things and the exact steps that show it: where, what is wrong, what good looks like. No steps, no finding: it is a note. Do not manufacture findings; a clean pass is a pass. Details and examples: `references/findings.md`.

## The pass rule

A loop passes only when all three hold:

1. Every desk's score is at or above the bar.
2. No blocking or major finding is open.
3. Every desk was audited by the audit model (a desk that failed its first pass is never a pass).

## The flow

```
prove --> first pass, every desk (work model)
              |
     desk at the bar, no blocking/major?
        yes |                 | no
            v                 v
   final audit (audit model)  straight to fixers
            \               /
             record: one log per loop
                     |
        pass rule met? --yes--> done
                     | no
        fixers (work model) --> one check step --> next loop
                     |
        cap reached? stop, carry open items to the next run
```

- **Prove.** Run it for real (tests, the app, the endpoint). A review that only reads a check certifies the intent; only running it certifies the artifact. Quote real output and exit codes. If a proof cannot run, that is a finding.
- **Reviews run after builders**, never beside them. A fix waits for the reviews in flight against that tree; if a fix has to land, discard those verdicts and re-run.
- **Record.** One log per loop, from the template in `references/findings.md`.
- **Fixers** fix every open blocking, major and minor, and cheap notes. **One check step** runs build, lint and tests once for all fixers.
- **Limits.** If every desk in a loop comes back empty (agents failed, usually an account or rate limit), the script stops and the next run carries that loop. Never let a loop record results from failed agents.
- **Cap.** Three loops by default. Raise it per run, never silently. Open items carry forward at their severity until closed with proof.

## Models

| Job | Default | Setting |
|---|---|---|
| Prove, first pass, record, fixers, check | `claude-sonnet-5-5` | `workModel` |
| Final audit, only for desks at the bar | `claude-opus-5-5` | `auditModel` |

Read the ids from the session's model list. Never guess an id, and never copy one from an old note; a wrong id fails every agent in the run.

## Cost rules

- Route only the desks the change touches (`references/desks.md`). Every desk you add is one more agent start.
- An agent start costs tens of thousands of tokens before it does any work. Fewer, bigger agents beat many tiny ones: one desk reviews a whole change, not one file.
- Run desks in chunks (`chunk`, default 4) so a small machine or a rate limit is not swamped.
- Do not spend the audit model on a desk that will fail anyway. That is the whole point of audit-only-at-the-bar.
- Small edits and records need no desk. Use desks for work that decides something or reaches a user.

## How to run it

**A. The workflow script** (needs Claude Code with the Workflow tool).

1. Copy `scripts/review-loop.js` out of the skill folder to a scratch path (a running script must not be edited).
2. Launch it with the Workflow tool: `scriptPath` = that copy, `args` = your settings (at least `root` and `scope`).
3. Or bake a settings file into a run copy: `python3 scripts/make-run.py scripts/review-loop.js .claude/scored-review-loop.json /scratch/run.js my-run`, then launch the copy by path with no pasted args.

**B. By hand in a session.** No Workflow tool needed.

1. Run the proof yourself.
2. Launch one Agent per desk in a chunk, each with the desk's lens, the bar words, the findings schema, and `model` set to the work model (the id, or the alias your Agent tool accepts, read from the session's model list).
3. For each desk at the bar with no blocking or major finding, launch one Agent on the audit model (same id or alias rule) with the first-pass findings.
4. Write the loop log. Send open findings to fixers on the work model. Run one check. Repeat up to the cap.

## The settings file

Looked for at `.claude/scored-review-loop.json` in the repo. Read it first. The workflow script cannot read files, so either pass the file's contents as `args` or bake it in with `make-run.py`. Its keys are the script's args. Example: `scored-review-loop.example.json`.

| Key | Meaning |
|---|---|
| `root` | Absolute path of the tree to review (required for the script) |
| `appDir` | App folder inside root, if any |
| `name`, `card` | Log slug; task id that starts every agent label |
| `scope`, `readFirst`, `files` | What the work is; records to read first; files fixers may touch |
| `desks` | Desk keys from the catalog, or full objects `{key, lens, first, final}` |
| `rolesDir` | Folder of role files, one `<role>.md` per desk role (see `references/role-template.md`) |
| `bar`, `barWords`, `cap`, `chunk`, `startLoop` | Pass score, bar words, loops, desks at once, first loop number |
| `workModel`, `auditModel` | Model ids |
| `prove`, `skipFirstProve`, `checkCommands` | Proof instructions (or `false`), reuse an existing proof, the check step's commands |
| `heavySlot`, `memoryRules`, `stackNotes`, `commonRules` | Optional text added to every brief |
| `logDir`, `indexFile`, `commitAfterCheck` | Where logs go; optional index to add a row to; commit after the check |
| `fixFirst`, `priorFindingsFile`, `priorResults` | Fix the previous loop's findings before the first loop of this run; the file path, or the prior desk results in memory |
| `order` | The owner's words behind this work, quoted in the relay guard |
| `areas` | Map `{name: [files]}` to run fixers in parallel by file group; default one group holding `files` |
| `proverRole`, `fixerRole`, `recorderRole` | Role file names in `rolesDir` for the proof runner, the fixers and the log writer |
| `relayGuard` | Replaces the default guard against chat lines being taken as instructions |

## Never

- Never pass a loop while any desk went unaudited, and never spend the audit model on a desk that failed its first pass.
- Never let a desk rule outside its lens or sign off on another desk's work.
- Never guess a model id.
- Never call a proof done unless it ran and its output is quoted.
- Never drop an open finding without proof it is closed; carry it.
- Never route every desk on every change.
- Never let reviewers edit files; only fixers write, and only their listed files.
- Never put secrets in a settings file or a brief.
