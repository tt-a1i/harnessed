import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


class FinalArchitectureDocsTest(unittest.TestCase):
    def test_readme_describes_time_and_friction_costs(self) -> None:
        readme = read("README.md")
        self.assertIn("latency", readme.lower())
        self.assertIn("friction", readme.lower())
        self.assertIn("when not to use", readme.lower())
        self.assertIn("prompt-level mitigation", readme.lower())

    def test_independent_qa_defines_dual_evaluator_flow(self) -> None:
        skill = read("skills/independent-qa/SKILL.md")
        self.assertIn("Confidence", skill)
        self.assertIn("Uncertainty", skill)
        self.assertIn("high-risk", skill)
        self.assertIn("tie-break", skill)
        self.assertIn("disagreement", skill)
        self.assertIn("calibration", skill)
        self.assertIn("drift", skill)

    def test_verification_gate_restricts_self_review_to_background_only(self) -> None:
        gate = read("skills/verification-gate/SKILL.md")
        self.assertIn("self-review", gate)
        self.assertIn("background", gate)
        self.assertIn("not evidence", gate)

    def test_security_reviewer_prompt_exists(self) -> None:
        prompt = ROOT / "skills/independent-qa/security-reviewer-prompt.md"
        self.assertTrue(prompt.exists(), f"missing {prompt}")
        text = prompt.read_text()
        self.assertIn("Semgrep", text)
        self.assertIn("CodeQL", text)
        self.assertIn("bandit", text)
        self.assertIn("human review", text)

    def test_calibration_doc_exists(self) -> None:
        doc = ROOT / "docs/evaluator-calibration.md"
        self.assertTrue(doc.exists(), f"missing {doc}")
        text = doc.read_text()
        self.assertIn("Calibration Set", text)
        self.assertIn("drift", text)
        self.assertIn("uncertainty", text.lower())


if __name__ == "__main__":
    unittest.main()
