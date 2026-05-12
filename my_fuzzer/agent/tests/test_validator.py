import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from my_fuzzer.agent.validator import parse_planner_output


class TestValidator(unittest.TestCase):
    def test_parse_planner_output_includes_line_target_hints(self):
        parsed = parse_planner_output(
            """
            {
              "analysis": "Need more png and language coverage",
              "reachable_by_grammar": ["sample.py:2 can be hit with lang query syntax"],
              "line_target_hints": [
                {
                  "target": "sample.py:2",
                  "delivery": "grammar",
                  "code_signal": "checks for query key `lang`",
                  "required_inputs": "query key `lang` with a language code value",
                  "grammar_implication": "allow `lang=<code>` where search parameters are emitted"
                }
              ],
              "recommended_rule_edits": [
                {"rule": "searchparameter", "rationale": "emit explicit lang key/value pairs"}
              ],
              "request_space_recommendations": {
                "host_profiles": [],
                "ua_profiles": [],
                "language_profiles": ["accept-language-en"],
                "ip_profiles": []
              }
            }
            """
        )

        self.assertEqual(parsed.analysis, "Need more png and language coverage")
        self.assertEqual(parsed.line_target_hints[0]["target"], "sample.py:2")
        self.assertEqual(parsed.line_target_hints[0]["delivery"], "grammar")
        self.assertIn("lang", parsed.line_target_hints[0]["required_inputs"])


if __name__ == "__main__":
    unittest.main()
