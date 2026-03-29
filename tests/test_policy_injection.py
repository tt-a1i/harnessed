import unittest
from pathlib import Path

from core.lib.policy_selection import POLICY_DIR, relevant_policy_paths


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


class PolicySelectionTest(unittest.TestCase):
    def test_service_changes_select_service_bundle(self) -> None:
        result = relevant_policy_paths(["services/order_service.py"])
        self.assertEqual(
            result,
            [
                f"{POLICY_DIR}/db.md",
                f"{POLICY_DIR}/response.md",
                f"{POLICY_DIR}/validation.md",
            ],
        )

    def test_auth_and_tests_add_domain_specific_policies(self) -> None:
        result = relevant_policy_paths(
            [
                "services/auth_service.py",
                "tests/test_auth_service.py",
            ]
        )
        self.assertEqual(
            result,
            [
                f"{POLICY_DIR}/auth.md",
                f"{POLICY_DIR}/db.md",
                f"{POLICY_DIR}/response.md",
                f"{POLICY_DIR}/testing.md",
                f"{POLICY_DIR}/validation.md",
            ],
        )

    def test_security_keywords_add_security_policy(self) -> None:
        result = relevant_policy_paths(
            ["api/routes/orders.py"],
            diff_text="+ if not user.is_admin: raise PermissionError('authz failed')",
        )
        self.assertIn(f"{POLICY_DIR}/security.md", result)

    def test_unmatched_changes_keep_existing_behavior(self) -> None:
        self.assertEqual(relevant_policy_paths(["docs/readme.md"]), [])


class PolicyDocumentationTest(unittest.TestCase):
    def test_contract_writing_mentions_policy_directory_and_selection(self) -> None:
        skill = read("skills/contract-writing/SKILL.md")
        self.assertIn(".harnessed/policies/", skill)
        self.assertIn("relevant policy", skill.lower())

    def test_evaluator_prompt_and_skill_define_relevant_policies_placeholder(
        self,
    ) -> None:
        prompt = read("skills/independent-qa/evaluator-prompt.md")
        skill = read("skills/independent-qa/SKILL.md")
        self.assertIn("{RELEVANT_POLICIES}", prompt)
        self.assertIn("Relevant Policies", prompt)
        self.assertIn("{RELEVANT_POLICIES}", skill)

    def test_artifact_protocol_mentions_policy_store(self) -> None:
        protocol = read("core/docs/artifact-protocol.md")
        self.assertIn("policies/", protocol)
        self.assertIn("policy", protocol.lower())


if __name__ == "__main__":
    unittest.main()
