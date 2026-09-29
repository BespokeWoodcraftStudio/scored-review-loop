# review-desks

A Claude Code skill for judging finished build work with review desks.

- Each desk has one lens and scores the work 0 to 100 against your bar words (default: functional, professional, premium, clean, easy to use).
- A cheap model does the first pass, the fixing and the paperwork. The strong model audits only the desks that are already at the bar.
- A loop passes only when every desk is at the bar, none has a blocking or major finding open, and every desk was audited.
- Findings go to fixers, one check step runs, and the loop repeats up to a cap.

## Install in a repo (project skill, not global)

```
git clone https://github.com/BespokeWoodcraftStudio/review-desks.git /tmp/review-desks
mkdir -p <repo>/.claude/skills && rsync -a --exclude .git /tmp/review-desks/ <repo>/.claude/skills/review-desks/
cp <repo>/.claude/skills/review-desks/review-desks.example.json <repo>/.claude/review-desks.json
```

Edit `.claude/review-desks.json`: root, scope, desks, prove, checkCommands. Leave `.git` out of the copy, or `git add` records an embedded repo and teammates get no files.

It loads as a project skill in that repo only. It is not installed in your home folder, so no other repo sees it. To use it in another repo, run the same three lines there. Commit `.claude/skills/review-desks` and `.claude/review-desks.json` if you want the team to share them.

## Run a review loop

Option A, the workflow script. Needs Claude Code with the Workflow tool.

1. Copy `scripts/review-loop.js` to a scratch path.
2. Ask Claude to run it with the Workflow tool, `args` taken from `.claude/review-desks.json`.
3. Or bake the settings in and launch the copy by path:
   `python3 .claude/skills/review-desks/scripts/make-run.py .claude/skills/review-desks/scripts/review-loop.js .claude/review-desks.json /scratch/run.js my-run`

Option B, by hand. No Workflow tool. Tell Claude "review this with the review-desks skill" and it launches one agent per desk with the Agent tool, using the models below (the model id, or the alias your Agent tool accepts, from the session's model list). `SKILL.md` has the steps.

Logs land in `logDir` (default `docs/review-log`), one per loop.

## Change the models

Set `workModel` and `auditModel` in `.claude/review-desks.json`. Defaults are `claude-sonnet-5-5` and `claude-opus-5-5`. Read the ids from your session's model list; do not guess, a wrong id fails every agent.

## Add your own desks

Put role files in a folder, set `rolesDir` to it, and add desk objects to `desks`. See `references/role-template.md` and `references/desks.md`.

## Files

| File | What it is |
|---|---|
| `SKILL.md` | The skill: trigger, desk model, score, severities, pass rule, flow, cost rules |
| `references/desks.md` | Default desks and how to route only the ones a change touches |
| `references/findings.md` | Severities with examples, findings JSON, loop log template, carry rule |
| `references/role-template.md` | Template for a desk role file |
| `scripts/review-loop.js` | The generic workflow script |
| `scripts/make-run.py` | Bakes a settings file into a copy of the script |
| `review-desks.example.json` | Example settings for a generic web app |

## Requirements

- Claude Code.
- The Workflow tool for option A. Option B needs only the Agent tool.
- Python 3 for `make-run.py`.

## License

Private, internal use only. Do not publish or redistribute.
