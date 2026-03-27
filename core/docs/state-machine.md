# QA State Machine

- `SHIP`: all automatable criteria pass and no manual-review items remain
- `SHIP_WITH_HUMAN_REVIEW`: all automatable criteria pass and at least one criterion requires human review
- `ITERATE`: fixable failures remain
- `BLOCKED`: critical issue, fundamentally flawed approach, or evaluator failure

## Precedence
`BLOCKED > ITERATE > SHIP_WITH_HUMAN_REVIEW > SHIP`
