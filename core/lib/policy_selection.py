from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

POLICY_DIR = ".harnessed/policies"

POLICY_ORDER = (
    "auth.md",
    "db.md",
    "response.md",
    "security.md",
    "testing.md",
    "validation.md",
)


@dataclass(frozen=True)
class PolicyRule:
    path_keywords: tuple[str, ...] = ()
    path_suffixes: tuple[str, ...] = ()
    diff_keywords: tuple[str, ...] = ()
    policies: tuple[str, ...] = ()

    def matches(self, changed_paths: Iterable[str], diff_text: str) -> bool:
        normalized_paths = [path.lower().replace("\\", "/") for path in changed_paths]
        normalized_diff = diff_text.lower()

        for path in normalized_paths:
            if any(keyword in path for keyword in self.path_keywords):
                return True
            if any(path.endswith(suffix) for suffix in self.path_suffixes):
                return True

        return any(keyword in normalized_diff for keyword in self.diff_keywords)


RULES = (
    PolicyRule(
        path_keywords=("auth", "session", "permission"),
        diff_keywords=(
            "authz",
            "authorization",
            "authentication",
            "require_auth",
            "permissionerror",
        ),
        policies=("auth.md",),
    ),
    PolicyRule(
        path_keywords=("service", "services/", "api/", "route", "endpoint"),
        path_suffixes=("_service.py", ".service.ts", ".service.js"),
        policies=("db.md", "response.md", "validation.md"),
    ),
    PolicyRule(
        path_keywords=("tests/", "/test", "spec", "fixture"),
        path_suffixes=("_test.py", ".test.ts", ".test.js", ".spec.ts", ".spec.js"),
        policies=("testing.md",),
    ),
    PolicyRule(
        path_keywords=("security", "crypto", "secret"),
        diff_keywords=(
            "xss",
            "csrf",
            "sql injection",
            "secrets",
            "unsafe",
            "sanitize",
            "escape",
            "permissionerror",
        ),
        policies=("security.md",),
    ),
)


def relevant_policy_paths(
    changed_paths: Iterable[str], diff_text: str = ""
) -> list[str]:
    selected: set[str] = set()

    for rule in RULES:
        if rule.matches(changed_paths, diff_text):
            selected.update(rule.policies)

    return [f"{POLICY_DIR}/{name}" for name in POLICY_ORDER if name in selected]
