import unittest

from triage import build_issue_text, recommend_priority, triage_issue


class TriageHelpersTests(unittest.TestCase):
    def test_build_issue_text_combines_title_and_body(self):
        result = build_issue_text("PDF crashes", "Upload fails.")
        self.assertIn("Issue title: PDF crashes", result)
        self.assertIn("Issue description: Upload fails.", result)

    def test_build_issue_text_handles_empty_title(self):
        self.assertEqual(build_issue_text("", "Only body"), "Only body")

    def test_priority_critical_for_exposed_credentials(self):
        priority, reason = recommend_priority("Password in plain text in logs")
        self.assertEqual(priority, "Critical")
        self.assertTrue(reason)

    def test_priority_high_for_crash(self):
        priority, _ = recommend_priority("Application crashes when opening settings")
        self.assertEqual(priority, "High")

    def test_priority_low_is_explicitly_heuristic(self):
        priority, reason = recommend_priority("Please add a new theme option")
        self.assertEqual(priority, "Low")
        self.assertIn("suggestion", reason)

    def test_triage_ranks_bug_keywords_and_returns_relative_scores(self):
        result = triage_issue("App crashes when uploading a PDF")
        self.assertEqual(result["labels"][0], "bug")
        self.assertAlmostEqual(sum(result["scores"]), 1.0)

    def test_triage_recognizes_feature_and_documentation_keywords(self):
        feature = triage_issue("Please add a dark mode option")
        documentation = triage_issue("The installation guide is missing setup steps")
        self.assertEqual(feature["labels"][0], "feature-request")
        self.assertEqual(documentation["labels"][0], "documentation")

    def test_triage_falls_back_to_question_for_unmatched_text(self):
        result = triage_issue("The moon is bright tonight")
        self.assertEqual(result["labels"][0], "question")
        self.assertEqual(result["scores"][0], 1.0)


if __name__ == "__main__":
    unittest.main()
