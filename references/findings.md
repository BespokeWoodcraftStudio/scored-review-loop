# Findings, severities, the loop log

## Severity definitions

| Severity | Definition | Example |
|---|---|---|
| blocking | The work cannot be used or is unsafe. A real person or run hits it | Saving a form throws an error and loses the entry. Steps: open Settings, edit the name, press Save |
| major | Real harm in a plausible case | The list shows another user's rows when two users share a team. Steps: sign in as user B, open Reports |
| minor | A rough edge a real person could hit; no harm | The empty state has no message, only a blank area. Steps: open Reports with no data |
| note | A preference, or a case nobody meets | Would prefer a different icon; a path that only exists if the clock is set to year 2100 |

A finding is only blocking, major or minor if it comes with the exact steps a real person or a real run takes to hit it. Without steps it is a note.

Do not manufacture findings. A desk that always finds something teaches the team to skim, and the finding that mattered goes past.

## The findings JSON the desks return

```json
{
  "desk": "qa",
  "score": 84,
  "verdict": "fail",
  "findings": [
    {
      "id": "QA-L1-001",
      "severity": "major",
      "where": "src/reports/list.tsx, the Reports screen",
      "wrong": "With two users on one team, user B sees user A's rows. Steps: sign in as B, open Reports.",
      "good": "Each user sees only rows they may read, and a test proves it."
    }
  ]
}
```

- `verdict` is `pass` only when the score is at or above the bar and there is no blocking or major finding.
- Ids run `DESKKEY-L<loop>-001` onward.

## Loop log template

File: `<logDir>/loop-<n>-<name>.md`

```
# Loop <n>: <name>

## Desks
| Desk | Score | Pass or fail | Decided by | Blocking | Major | Minor |
|---|---|---|---|---|---|---|
| code | 92 | pass | final audit | 0 | 0 | 1 |
| qa | 84 | fail | first pass | 0 | 1 | 2 |

## Open findings (blocking first)
| Id | Desk | Severity | Where | Wrong | Good |
|---|---|---|---|---|---|

## Bar
Bar 90. PASSED only if every desk was audited at or above the bar and no blocking or major finding is open.
Result: FAIL (qa at 84, one major open, qa not audited).

## Fixed in loop <n>
| Id | What changed | Where | Proof |
|---|---|---|---|
```

"Decided by" is `final audit` when the audit model ruled, `first pass` when the desk failed and was not audited.

## The carry rule

- Every open item is carried into the next loop's log at its severity until it is closed with proof.
- Closed with proof means the named check ran and its output shows the fix, quoted in the "Fixed in loop" table. "Fixed in code" without a run is not closed.
- A reviewer checks every item the previous log says was fixed. An item not really fixed comes back at the same severity.
- Nothing is dropped because the cap was reached. Open items carry into the next run's first log.
