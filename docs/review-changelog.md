# Review Changelog

100 improvements across 9 review rounds. Each entry documents an issue found and fixed during iterative subagent-driven review.

---

## Round 1: Structural Review

| # | Issue | Fix |
|---|-------|-----|
| 1 | hooks/ directory inside .claude-plugin/ (wrong location) | Moved to plugin root |
| 2 | hooks.json used flat array format instead of three-level nesting | Rewritten to matcher/hooks/type format |
| 3 | plugin.json author as bare string | Changed to object `{"name": "Harnessed"}` |
| 4 | Hook output missing hookEventName field | Added `"hookEventName": "SessionStart"` |
| 5 | session-start fallback path wrong (../../ instead of ../) | Fixed relative path |
| 6 | All 4 SKILL.md descriptions contained workflow summaries (CSO violation) | Trimmed to triggering conditions only |
| 7 | Meta-skill too large (~800 words) for session injection | Moved detail to reference.md, reduced to ~648 words |

## Round 2: Functional Review

| # | Issue | Fix |
|---|-------|-----|
| 8 | Contract-writing missing minimum criterion rule | Added: every contract must have at least 1 criterion |
| 9 | Independent-qa missing empty diff handling | Added: STOP if git diff produces no output |
| 10 | Independent-qa missing non-git repo handling | Added: collect full file contents as fallback |
| 11 | Verification-gate missing micro task path | Added: lighter verification for micro tasks |
| 12 | Evaluator prompt missing MANUAL_REVIEW_NEEDED grade | Added as per-criterion grade option |
| 13 | No guidance for handling requirement changes mid-task | Added: update contract, re-run QA |
| 14 | Grading rubric missing concrete examples | Added examples for each grade level |

## Round 3: Usage Simulation

| # | Issue | Fix |
|---|-------|-----|
| 15 | Meta-skill lacks artifact lifecycle management | Added: archive stale artifacts on new task |
| 16 | No task disambiguation (new vs continuation) | Added: ask user when ambiguous |
| 17 | Missing timestamp format for archive files | Specified: YYYYMMDD-HHMMSS |
| 18 | Evaluator could see generator reasoning via conversation context | Strengthened context isolation instructions |
| 19 | No guidance for committed-but-not-diffable changes | Added: suggest `git diff HEAD~1` |
| 20 | Contract-writing missing refactor classification guidance | Clarified: refactors need regression criteria |
| 21 | Verification-gate Step 3 gap checklist incomplete | Added: check for unresolved ITERATE/BLOCKED |

## Round 4: Competitive Analysis (vs Superpowers, Cursor Rules, Aider)

| # | Issue | Fix |
|---|-------|-----|
| 22 | README lacked compelling value proposition | Rewrote with statistics and pipeline diagram |
| 23 | No example QA report in README | Added realistic localStorage key mismatch example |
| 24 | Installation instructions incomplete | Added git clone + cp + chmod steps |
| 25 | No .gitignore for .harnessed/ artifacts | Created .gitignore + documented in README |
| 26 | Missing LICENSE file | Added MIT license |
| 27 | No cost estimate for users | Added: ~1.5x token usage section |
| 28 | Design principles not articulated | Added 4 principles (Verification > Process, etc.) |
| 29 | Skills table missing from README | Added with invocation and purpose columns |
| 30 | Complementary mode explanation unclear in README | Added dedicated section |

## Round 5: Architectural Threat Model

| # | Issue | Fix |
|---|-------|-----|
| 31 | "Execution result wins" rule dangerous (shared assumptions) | Changed to asymmetric rule: execution FAIL wins, but PASS doesn't dismiss code review |
| 32 | No pre-flight checks before expensive evaluator dispatch | Added Step 2b: run linter/type-check/tests first |
| 33 | Subagent permissions wrong (read+execute, missing write) | Fixed to read, write, and execute |
| 34 | Priority hierarchy vs HARD-GATE contradiction | Clarified: HARD-GATEs prevent agent rationalization, not user override |
| 35 | Contract gaming risk undocumented | Documented in roadmap: contract review step planned |
| 36 | Same-model blind spots undocumented | Documented in roadmap: cross-model eval planned |
| 37 | Evaluator attention ceiling undocumented | Documented as known inherent limitation |
| 38 | No roadmap for future improvements | Created docs/roadmap-v1.md |
| 39 | Config values hardcoded with no override path | Documented in roadmap: config file planned |
| 40 | No security checklist for auth/input criteria | Documented in roadmap: security addendum planned |

## Round 6: Deep Semantic Review (Opus 4.6)

| # | Issue | Fix |
|---|-------|-----|
| 41 | Evaluator framed as "skeptical engineer" (negativity bias) | Reframed as "independent code auditor" (evidence-based) |
| 42 | Asymmetric execution rule described in prose (hard to parse) | Reformatted as table |
| 43 | No quality constraint on evaluator output | Added: each finding must be detailed enough for unfamiliar developer |
| 44 | Anti-rationalization missing "impatient user" pattern | Added: "User impatience is about communication, not quality" |
| 45 | Anti-rationalization missing "second attempt" pattern | Added: "Knowing the previous failure doesn't guarantee the fix is correct" |
| 46 | Anti-rationalization missing "no tests" pattern | Added: "Tier 1 code review alone catches logic errors" |
| 47 | Contract-writing missing requirement changes section | Added: update contract, assess existing code, re-run QA |
| 48 | Contract-writing missing refactor classification | Added: "Refactors have the strictest contract: behavior must be IDENTICAL" |
| 49 | Grading rubric PASS lacked concrete example | Added: API 404 check example |
| 50 | Grading rubric PARTIAL lacked concrete example | Added: case-insensitive search Unicode example |
| 51 | Grading rubric FAIL lacked concrete example | Added: plaintext password storage example |
| 52 | Grading rubric MANUAL_REVIEW_NEEDED lacked concrete example | Added: dark mode visual consistency example |
| 53 | SHIP grade definition did not exclude MANUAL_REVIEW_NEEDED | Added: "Criteria graded MANUAL_REVIEW_NEEDED are excluded from this count" |
| 54 | Evaluator prompt "cut corners" phrase not in implementation | Removed from spec (spec drift, fixed in Round 8) |
| 55 | Missing iteration count persistence guidance | Added to SKILL.md (improved in Round 7) |
| 56 | Contract format embedded inline (no single source of truth) | Extracted in Round 9 |
| 57 | Context budget heuristic vague | Clarified in Round 9 |
| 58 | Evaluator timeout/token limits unaddressed | Addressed via Step 4b retry mechanism |

## Round 7: Lifecycle Edge Cases, Data Flow, Extensibility

| # | Issue | Fix |
|---|-------|-----|
| 59 | **[BROKEN]** Iteration count appended to qa-report.md, overwritten by evaluator | Created separate `.harnessed/qa-state.md` for persistence |
| 60 | **[BROKEN]** MANUAL_REVIEW_NEEDED criteria block verification-gate (deadlock) | Added exception: listed under "Pending Human Review" section |
| 61 | Complementary mode: verification-gate reads raw spec, evaluator gets normalized contract | Both now read from `.harnessed/contract.md` in all modes |
| 62 | {VERIFICATION_COMMANDS} empty in complementary mode | Synthesis instructions now require generating verification commands |
| 63 | Git diff command ambiguous ("staged + unstaged" but no exact command) | Specified `git diff HEAD` throughout |
| 64 | qa-report.md staleness check prescribed but mechanism undefined | Defined: compare file mtime against `dispatched_at` in qa-state.md |
| 65 | Concurrent sessions clobber `.harnessed/` artifacts silently | Documented as unsupported in README and reference.md |
| 66 | Hook silent failure (exits 0 with garbage JSON, agent unaware) | Added output validation before JSON emission |
| 67 | No merge conflict detection before QA dispatch | Added Step 2c: check `.git/MERGE_HEAD` |
| 68 | {MODE} placeholder missing for future per-criterion evaluation | Added to evaluator-prompt.md and SKILL.md placeholder list |
| 69 | Contract format duplicated (inline in SKILL.md, no single source) | Created `contract-format.md` as standalone reference |
| 70 | Verification-gate summary template missing "Pending Human Review" section | Added section for MANUAL_REVIEW_NEEDED criteria |
| 71 | qa-state.md missing from artifact directory listings | Added to README.md and reference.md |
| 72 | Concurrent sessions note missing from reference.md | Added alongside directory listing |

## Round 8: Spec Drift + Developer Experience

### Spec.md sync (16 drifts)

| # | Issue | Fix |
|---|-------|-----|
| 73 | qa-state.md missing from File Communication Protocol table | Added row |
| 74 | qa-report.md author ambiguous ("independent-qa" vs evaluator subagent) | Clarified: "evaluator subagent (dispatched by independent-qa)" |
| 75 | Iteration mechanism describes wrong persistence (qa-report.md not qa-state.md) | Updated with qa-state.md format and compaction-survival rationale |
| 76 | Evaluator persona: spec says "skeptical senior engineer", implementation says "code auditor" | Updated spec to "independent code auditor" |
| 77 | Spec quotes nonexistent evaluator text ("cut corners") | Updated to actual text |
| 78 | Tier 2 indicators incomplete (missing go.mod, tests/ dir, specific ports) | Added all indicators with commands |
| 79 | Complementary mode flow wrong (spec says skip contract.md, impl writes it) | Updated to reflect contract.md written in both modes |
| 80 | Pre-flight checks (Step 2b) not in spec | Added section |
| 81 | Git state checks (Step 2c) not in spec | Added section |
| 82 | Evaluator output verification (Step 4b) not in spec | Added section |
| 83 | Context budget management not in spec | Added ~80K token budget with fallback strategies |
| 84 | Non-git repository handling not in spec | Added fallback description |
| 85 | Artifact lifecycle (archiving) not in spec | Added section |
| 86 | MANUAL_REVIEW_NEEDED effect on overall grade not described | Added: excluded from count, does not block SHIP |
| 87 | contract-format.md missing from plugin structure tree | Added to tree |
| 88 | Hook matcher, Cursor support, "priority tags" claim inaccurate | Updated loading mechanism section |

### README DX improvements

| # | Issue | Fix |
|---|-------|-----|
| 89 | "What It Does" preamble repeats "Why" section | Tightened to one-line lead-in |
| 90 | Installation as single cp command, no verification step | Restructured: Option A/B, numbered post-install steps |
| 91 | .gitignore step easy to miss (afterthought paragraph) | Made numbered installation step |
| 92 | No way to verify installation worked | Added: `bash harnessed/hooks/session-start` verification |
| 93 | chmod instruction on wrong path + redundant after git clone | Moved to blockquote note for zip downloads only |
| 94 | No documentation on how to opt out of QA | Added Customization section (skip QA, skip contract, disable entirely) |
| 95 | No troubleshooting section | Added: 4 common failure modes with solutions |
| 96 | Artifacts tree missing archive/ subdirectory | Added to tree |

## Round 9: Final Polish

| # | Issue | Fix |
|---|-------|-----|
| 97 | No guidance for binary files in git diff (non-diffable assets) | Added: note binary changes to evaluator, mark as MANUAL_REVIEW_NEEDED |
| 98 | "Iron Law" terminology in spec.md/plan.md, "HARD-GATE" in skill files | Unified to HARD-GATE across all files |
| 99 | Orchestrator notes section ambiguous (might be sent to evaluator) | Added bold note: "Do NOT send to evaluator subagent" |
| 100 | `lsof` not available on all Linux distros | Added `ss -tlnp` as Linux alternative |
| 101 | "Auto-generated files" in context budget vague | Added concrete examples (lock files, minified, dist/, build/, API clients) |
| 102 | qa-state.md not included in artifact archival lifecycle | Added as step 3 in archive sequence |

---

## Summary by Category

| Category | Count |
|----------|-------|
| Data flow / state management fixes | 12 |
| Edge case handling | 14 |
| Anti-rationalization patterns | 6 |
| Spec/docs sync | 20 |
| Developer experience | 12 |
| Evaluator quality | 10 |
| Plugin structure / hooks | 8 |
| Contract/grading system | 10 |
| Competitive / positioning | 8 |
| **Total** | **100** |
