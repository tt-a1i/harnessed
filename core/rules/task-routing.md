# Task Routing Rules

Canonical routing policy used by `using-harnessed` across all adapters.

## Operating Modes

- **Standalone Mode**: run `contract-writing` before implementation.
- **Complementary Mode**: if Superpowers specs exist, skip local contract drafting and normalize the spec into `.harnessed/contract.md`.
- **Micro Task**: skip contract and QA, but still run the verification gate.

## Size Routing

| Task Size | Indicators | Pipeline |
|-----------|-----------|----------|
| Micro | single-line fix, typo, comment-only, inert config tweak | code -> verification-gate |
| Standard | bug fix, function, component, API, focused refactor | contract -> code -> QA -> gate |
| Large | new feature, multi-file refactor, public interface change | contract -> user review -> code -> QA -> gate |

## Canonical Rule

When in doubt, treat the task as Standard.
