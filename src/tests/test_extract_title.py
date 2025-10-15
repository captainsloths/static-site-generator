import unittest
from markdown_blocks import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_other_content(self):
        markdown = """# My Title

This is some paragraph text.

## This is h2

More text here."""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_not_first_line(self):
        markdown = """Some text before

# The Real Title

More content"""
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_extract_title_no_h1(self):
        markdown = """## This is h2

### This is h3

No h1 here!"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_with_inline_markdown(self):
        markdown = "# **Bold** Title with *italic*"
        self.assertEqual(extract_title(markdown), "**Bold** Title with *italic*")

    def test_extract_title_multiple_h1(self):
        markdown = """# First Title

## Some h2

# Second Title"""
        # Should return the first h1
        self.assertEqual(extract_title(markdown), "First Title")


if __name__ == "__main__":
    unittest.main()
