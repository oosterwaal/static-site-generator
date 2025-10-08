import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_h1_not_first_line(self):
        md = "Some intro\n# Title Here\nMore text"
        self.assertEqual(extract_title(md), "Title Here")

    def test_multiple_h1(self):
        md = "# First Title\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("No header here\n## Subheading")

    def test_h1_with_special_chars(self):
        self.assertEqual(extract_title("# Hello @ 2025!"), "Hello @ 2025!")

    def test_h1_with_leading_spaces(self):
        self.assertEqual(extract_title("   # Leading"), "Leading")

if __name__ == "__main__":
    unittest.main()
