import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from my_fuzzer.agent.utils.llm_utils import (
    codebase_reachability_guide_formatter,
    missing_line_context_formatter,
)


class TestLLMUtils(unittest.TestCase):
    def test_missing_line_context_formatter_includes_source_excerpt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            source_file = repo_root / "sample.py"
            source_file.write_text(
                "def feature(query):\n"
                "    if \"lang\" in query:\n"
                "        return \"png\"\n"
                "    return None\n",
                encoding="utf-8",
            )
            coverage_data = {
                "files": {
                    "sample.py": {
                        "missing_lines": [2],
                        "functions": {
                            "feature": {
                                "missing_lines": [2],
                                "start_line": 1,
                            }
                        },
                    }
                }
            }
            config = SimpleNamespace(
                repo_root=repo_root,
                max_missing_files=5,
                max_missing_lines_per_file=5,
            )

            formatted = missing_line_context_formatter(
                coverage_data,
                config,
                max_files=1,
                max_lines_per_file=1,
            )

        self.assertIn("### sample.py", formatted)
        self.assertIn("Target line: 2", formatted)
        self.assertIn("Likely function: `feature`", formatted)
        self.assertIn("if \"lang\" in query:", formatted)

    def test_codebase_reachability_guide_contains_request_to_code_mappings(self):
        guide = codebase_reachability_guide_formatter()

        self.assertIn("Only use this guide for Python-covered modules", guide)
        self.assertIn("bin/srv.py:47-69", guide)
        self.assertIn("lib/wttr_srv.py:58-76", guide)
        self.assertIn("?debug=true", guide)
        self.assertIn("?format=3", guide)
        self.assertIn("Add to grammar:", guide)
        self.assertNotIn("internal/query/fromrequest.go", guide)


if __name__ == "__main__":
    unittest.main()
