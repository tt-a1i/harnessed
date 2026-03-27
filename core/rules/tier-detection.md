# Verification Tier Detection Rules

## Tier 1
- No test suite
- No running dev server
- Perform code review only

## Tier 1.5
- No test suite
- Running dev server detected on common ports
- Perform code review plus HTTP smoke tests

## Tier 2
- Test suite indicator present
- Perform code review plus execution verification

## Canonical Test Suite Indicators
- `package.json` with a non-placeholder `test` script
- `pytest.ini`
- `pyproject.toml` with `[tool.pytest]`
- `tests/` with test naming convention
- `Makefile` test target
- `go.mod`
- `playwright.config.*`
- `cypress.config.*`
