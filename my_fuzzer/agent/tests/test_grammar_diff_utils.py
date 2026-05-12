import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from my_fuzzer.agent.utils.grammar_diff_utils import build_grammar_diff, write_grammar_diff_report


class TestGrammarDiffUtils(unittest.TestCase):
    def test_build_grammar_diff_includes_rule_change(self):
        old_grammar = "grammar url;\nurl: HOSTNAME;\n"
        new_grammar = "grammar url;\nurl: HOSTNAME | PORTS;\n"

        diff_text = build_grammar_diff(old_grammar, new_grammar, "old", "new")

        self.assertIn("--- old", diff_text)
        self.assertIn("+++ new", diff_text)
        self.assertIn("-url: HOSTNAME;", diff_text)
        self.assertIn("+url: HOSTNAME | PORTS;", diff_text)

    def test_write_grammar_diff_report_writes_markdown_file(self):
        old_grammar = "grammar url;\nurl: HOSTNAME;\n"
        new_grammar = "grammar url;\nurl: HOSTNAME | PORTS;\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "grammar_report.md"
            write_grammar_diff_report(
                report_path,
                iteration=3,
                from_label="baseline",
                to_label="candidate",
                decision="promoted_to_champion",
                mutation_status="accepted",
                old_text=old_grammar,
                new_text=new_grammar,
                metadata={"Proposed Rules": ["url"]},
            )

            content = report_path.read_text(encoding="utf-8")

        self.assertIn("# Grammar Diff Report", content)
        self.assertIn("| Iteration | 3 |", content)
        self.assertIn("| Decision | promoted_to_champion |", content)
        self.assertIn("```diff", content)
        self.assertIn("+url: HOSTNAME | PORTS;", content)


if __name__ == "__main__":
    unittest.main()
