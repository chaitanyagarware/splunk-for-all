# Contributing To Splunk For All

Thank you for improving an open learning resource. Contributions should make a learner more accurate, confident, or effective.

## Good Contributions

- Correct an inaccurate SPL example or version-sensitive statement.
- Add an explanation that answers *why*, not only *what*.
- Add synthetic data and a lab that can be reproduced.
- Improve accessibility, navigation, diagrams, or plain-language clarity.
- Document Cloud and Enterprise differences without implying unsupported parity.

Do not contribute proprietary course material, exam questions, customer data, credentials, copyrighted screenshots, or examples copied from documentation without permission.

## Workflow

1. Open an issue for large changes so the scope can be discussed.
2. Fork the repository and create a focused branch.
3. Write examples using synthetic or thoroughly anonymized data.
4. Run `python scripts/validate_repo.py` from the repository root.
5. Open a pull request and explain the learner outcome.

## Lesson Style

New curriculum pages should include these headings when they apply:

```markdown
# Topic

## Learning Objectives
## Mental Model
## Core Patterns
## Worked Example
## Production Notes
## Practice
## Checkpoint
## Official Resources
```

Use fenced `spl` blocks for SPL. Prefer an explicit base search with `index`, `sourcetype`, and time guidance. Explain field assumptions near the query. Use placeholders such as `<index>` only in templates, not in examples a beginner is expected to run unchanged.

## SPL Review Checklist

- Does the query narrow data before expensive commands?
- Are field types and null behavior understood?
- Is the time range stated?
- Is high-cardinality grouping bounded?
- Does the example avoid `join` or `transaction` when `stats` is clearer?
- Are security searches framed as hypotheses requiring tuning and validation?
- Are risky administrative actions marked and paired with rollback guidance?

## Commit Messages

Use short, descriptive commits such as `docs: explain tstats constraints` or `labs: add failed-login investigation`. One conceptual change per commit is ideal.

By contributing, you agree that your contribution is licensed under this repository's MIT License.

