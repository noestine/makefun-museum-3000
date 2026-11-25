"""Tests for main.py — Museum of the Year 3000 entry.

The program writes one museum-label line to /output/entry.txt (or to a
path given on the command line). The sealed gate requires UTF-8 text of
1-200 characters, not only whitespace; the judge compares the single line
pairwise. Every test below is written from RULES.txt before main.py exists.
"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main as entry_main

REPO = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(REPO, "main.py")

EXPECTED = (
    "Smoke detector, c. 2025. A small ceiling god, fed a fresh battery "
    "twice a year and consulted only when dinner burned."
)


def run_main(out_path, cwd=None):
    """Run main.py with an explicit output path; return the process."""
    return subprocess.run(
        [sys.executable, MAIN, out_path],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestEntryText(unittest.TestCase):
    def test_output_file_exists_and_is_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(out, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8")  # raises if not valid UTF-8
            self.assertEqual(text, EXPECTED)

    def test_exact_line_and_char_count(self):
        self.assertEqual(len(EXPECTED), 117)
        self.assertEqual(len(EXPECTED.encode("utf-8")), 117)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED)

    def test_single_line_no_newline_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, encoding="utf-8") as fh:
                content = fh.read()
            self.assertNotIn("\n", content)
            self.assertNotIn("\r", content)
            self.assertEqual(content.count("\n"), 0)

    def test_gate_length_1_to_200(self):
        self.assertGreaterEqual(len(EXPECTED), 1)
        self.assertLessEqual(len(EXPECTED), 200)

    def test_not_only_whitespace(self):
        self.assertTrue(EXPECTED.strip())
        self.assertEqual(EXPECTED, EXPECTED.strip())

    def test_ascii_only(self):
        self.assertTrue(EXPECTED.isascii())

    def test_label_shape(self):
        # Reads like a real museum label: object + date, then one
        # straight-faced sentence ending in a period.
        self.assertTrue(EXPECTED.startswith("Smoke detector, c. 2025. "))
        self.assertTrue(EXPECTED.endswith("."))

    def test_deterministic_two_runs_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = os.path.join(tmp, "first.txt")
            second = os.path.join(tmp, "second.txt")
            self.assertEqual(run_main(first).returncode, 0)
            self.assertEqual(run_main(second).returncode, 0)
            with open(first, "rb") as fh:
                a = fh.read()
            with open(second, "rb") as fh:
                b = fh.read()
            self.assertEqual(a, b)

    def test_runs_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out, cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(out, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED)

    def test_overwrites_longer_previous_file_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write("x" * 500)
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED)

    def test_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nested", "deep", "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED)

    def test_default_path_writes_next_to_repo(self):
        # No argument: writes ./output/entry.txt relative to the repo root
        # (the grading sandbox mounts /output; locally this avoids root).
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, MAIN],
                cwd=REPO,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            default_out = os.path.join(REPO, "output", "entry.txt")
            try:
                with open(default_out, encoding="utf-8") as fh:
                    self.assertEqual(fh.read(), EXPECTED)
            finally:
                if os.path.exists(default_out):
                    os.remove(default_out)


class TestGateValidation(unittest.TestCase):
    """The program must never silently ship a gate-invalid label."""

    def test_validate_accepts_the_shipped_label(self):
        self.assertEqual(entry_main.validate_label(EXPECTED), EXPECTED)

    def test_validate_rejects_empty(self):
        with self.assertRaises(ValueError):
            entry_main.validate_label("")

    def test_validate_rejects_whitespace_only(self):
        with self.assertRaises(ValueError):
            entry_main.validate_label("   \n  ")

    def test_validate_rejects_over_200_chars(self):
        with self.assertRaises(ValueError):
            entry_main.validate_label("x" * 201)

    def test_validate_accepts_exactly_200_chars(self):
        self.assertEqual(entry_main.validate_label("x" * 200), "x" * 200)

    def test_validate_rejects_newline_inside(self):
        with self.assertRaises(ValueError):
            entry_main.validate_label("one\ntwo")

    def test_validate_rejects_non_string(self):
        with self.assertRaises(ValueError):
            entry_main.validate_label(None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
