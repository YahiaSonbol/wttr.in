import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from my_fuzzer.agent.utils.coverage_diff_utils import (
    aggregate_coverages,
    compute_coverage_diff,
    write_aggregate_coverage_report,
    write_coverage_diff_report,
)
from my_fuzzer.agent.utils.report_utils import write_unavailable_report


class TestCoverageDiffUtils(unittest.TestCase):
    def test_compute_coverage_diff_detects_line_changes(self):
        old_cov = {
            "files": {
                "app.py": {
                    "executed_lines": [1, 2, 3],
                    "missing_lines": [4, 5],
                }
            },
            "totals": {
                "percent_covered": 60.0,
                "covered_lines": 3,
                "missing_lines": 2,
                "num_statements": 5,
            },
        }
        new_cov = {
            "files": {
                "app.py": {
                    "executed_lines": [1, 2, 3, 4],
                    "missing_lines": [5],
                },
                "extra.py": {
                    "executed_lines": [10],
                    "missing_lines": [],
                },
            },
            "totals": {
                "percent_covered": 83.33,
                "covered_lines": 5,
                "missing_lines": 1,
                "num_statements": 6,
            },
        }

        diff = compute_coverage_diff(
            old_cov,
            new_cov,
            max_files=10,
            max_lines_per_file=10,
        )

        self.assertAlmostEqual(diff["coverage_percent_delta"], 23.33, places=2)
        self.assertEqual(diff["covered_lines_delta"], 2)
        self.assertEqual(diff["missing_lines_delta"], -1)
        self.assertEqual(diff["newly_covered_lines_by_file"]["app.py"], [4])
        self.assertEqual(diff["newly_covered_lines_by_file"]["extra.py"], [10])
        self.assertEqual(diff["no_longer_missing_lines_by_file"]["app.py"], [4])

    def test_write_reports_create_expected_markdown(self):
        diff_data = {
            "coverage_percent_old": 50.0,
            "coverage_percent_new": 75.0,
            "coverage_percent_delta": 25.0,
            "covered_lines_old": 10,
            "covered_lines_new": 15,
            "covered_lines_delta": 5,
            "missing_lines_old": 10,
            "missing_lines_new": 5,
            "missing_lines_delta": -5,
            "num_statements_old": 20,
            "num_statements_new": 20,
            "num_statements_delta": 0,
            "files_with_any_change": ["app.py"],
            "newly_covered_lines_by_file": {"app.py": [11, 12]},
            "no_longer_covered_lines_by_file": {},
            "newly_missing_lines_by_file": {},
            "no_longer_missing_lines_by_file": {"app.py": [13]},
            "files_with_new_coverage": 1,
            "files_with_new_missing": 0,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            coverage_report = Path(tmpdir) / "coverage_report.md"
            unavailable_report = Path(tmpdir) / "coverage_unavailable.md"

            write_coverage_diff_report(
                coverage_report,
                iteration=2,
                from_label="baseline",
                to_label="candidate",
                diff_data=diff_data,
                metadata={"Baseline Reference": "baseline_iteration_002"},
            )
            write_unavailable_report(
                unavailable_report,
                "Coverage Diff Report",
                "Candidate grammar was rejected during validation and was not executed.",
                {"Iteration": 2},
            )

            coverage_content = coverage_report.read_text(encoding="utf-8")
            unavailable_content = unavailable_report.read_text(encoding="utf-8")

        self.assertIn("# Coverage Diff Report", coverage_content)
        self.assertIn("| Coverage Delta | +25.00 |", coverage_content)
        self.assertIn("`app.py`: [11, 12]", coverage_content)
        self.assertIn("Status: not available", unavailable_content)
        self.assertIn("was not executed", unavailable_content)

    def test_aggregate_coverages_unions_executed_lines_across_iterations(self):
        coverage_items = [
            {
                "label": "iteration_001_baseline",
                "coverage_data": {
                    "files": {
                        "app.py": {
                            "executed_lines": [1, 2],
                            "missing_lines": [3, 4],
                        }
                    },
                    "totals": {},
                },
            },
            {
                "label": "iteration_001_candidate",
                "coverage_data": {
                    "files": {
                        "app.py": {
                            "executed_lines": [3],
                            "missing_lines": [4],
                        },
                        "extra.py": {
                            "executed_lines": [10],
                            "missing_lines": [11],
                        },
                    },
                    "totals": {},
                },
            },
        ]

        aggregate = aggregate_coverages(
            coverage_items,
            max_files=10,
            max_lines_per_file=10,
        )

        self.assertEqual(aggregate["source_count"], 2)
        self.assertAlmostEqual(aggregate["totals"]["percent_covered"], 66.66666666666666, places=2)
        self.assertEqual(aggregate["totals"]["covered_lines"], 4)
        self.assertEqual(aggregate["totals"]["missing_lines"], 2)
        self.assertEqual(aggregate["files"]["app.py"]["executed_lines"], [1, 2, 3])
        self.assertEqual(aggregate["files"]["app.py"]["missing_lines"], [4])
        self.assertEqual(aggregate["files"]["extra.py"]["missing_lines"], [11])

    def test_write_aggregate_coverage_report_creates_summary_markdown(self):
        aggregate_data = {
            "source_count": 2,
            "source_labels": ["iteration_001_baseline", "iteration_001_candidate"],
            "totals": {
                "percent_covered": 66.67,
                "covered_lines": 4,
                "missing_lines": 2,
                "num_statements": 6,
            },
            "files": {},
            "top_missing_lines_by_file": {"app.py": [4], "extra.py": [11]},
            "top_covered_lines_by_file": {"app.py": [1, 2, 3]},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            aggregate_report = Path(tmpdir) / "cycle_aggregate_coverage.md"
            write_aggregate_coverage_report(
                aggregate_report,
                aggregate_data=aggregate_data,
                metadata={"Run Slug": "run_20260511"},
            )
            content = aggregate_report.read_text(encoding="utf-8")

        self.assertIn("# Cycle Aggregate Coverage Report", content)
        self.assertIn("| Aggregate Coverage | 66.67% |", content)
        self.assertIn("- iteration_001_baseline", content)
        self.assertIn("`app.py`: [4]", content)


if __name__ == "__main__":
    unittest.main()
