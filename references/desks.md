# Default desk catalog

Each desk has a first-pass role (work model) and a final-audit role (audit model). Role names are defaults; a repo may rename them (`rolesDir` holds the role files, see `role-template.md`).

| Key | Lens | First pass | Final audit |
|---|---|---|---|
| `code` | Correctness on every path including failures, types, tests that prove what they claim, no dead code | code-reviewer | principal-code-reviewer |
| `qa` | Every control and state exercised; the proof passes against a real run; nothing loops or fails silently | qa-engineer | head-of-qa |
| `design` | The approved look built as drawn; every state designed; tokens used; light and dark; nothing unfinished | product-designer | head-of-design |
| `copy` | Every word plain, short, true, consistent; no internal codes; a first-time person needs no instructions | copy-editor | head-of-copy |
| `security` | No leaks; every action checks who is signed in; inputs are data, not instructions; abuse bounded | security-reviewer | security-engineer |
| `accessibility` | WCAG 2.2 AA; contrast; focus; keyboard; names and roles; no colour-only meaning; reduced motion | accessibility-auditor | principal-frontend-engineer |
| `domain-user` | A new person in the target role can use it from the screens alone; fits how they really work | domain-user-reviewer | head-of-domain |
| `compliance` | Inside the written rules the repo must obey (privacy, retention, consent, policy text it names) | compliance-reviewer | head-of-compliance |

## Route only the desks the change touches

Every desk you add is another agent start. Pick by what the diff touches.

| The change | Desks |
|---|---|
| Pure logic, a library, a script | `code`, `qa` |
| A screen or component | `code`, `qa`, `design`, `copy`, `accessibility` |
| Wording only | `copy` |
| An endpoint, auth, a permission, input handling | `code`, `security`, `qa` |
| A form users fill in | `code`, `qa`, `copy`, `accessibility`, plus `security` if it takes input from outside |
| A data model or migration | `code`, `security`, `compliance` if retention or privacy rules apply |
| A workflow a specialist uses daily | `code`, `qa`, `domain-user` |
| A release | `qa`, `security`, plus whatever the release touches |

Rules of thumb:

- A change no user sees needs no `design`, `copy` or `accessibility` desk.
- When unsure, start with `code` and `qa`; add a desk only when a finding shows the change reaches its lens.
- A record or a tiny edit needs no desk at all.

## Add a desk for your repo's own domain

1. Pick one lens the existing desks do not cover (for example: pricing accuracy, unit conversions, a clinical rule, a game balance rule).
2. Write two role files from `role-template.md`: a first pass and a final audit.
3. Add the desk as an object in the settings file:

```json
{
  "key": "pricing",
  "lens": "Functional: totals match the published price rules on every path, rounding is stated, discounts never stack unless the rules say so.",
  "first": "pricing-reviewer",
  "final": "head-of-pricing"
}
```

4. Add its key to `desks` for the changes it applies to, not to every run.

The domain lens is the one worth writing carefully: it catches the result that is technically perfect and wrong for the people who use it.
