import unittest
from inline_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph"])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """First block


Second block with extra newlines



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block with extra newlines",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_with_whitespace(self):
        md = """
  First block with leading spaces

  Second block with trailing spaces

Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with leading spaces",
                "Second block with trailing spaces",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_heading(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_code_block(self):
        md = """Regular paragraph

```
def hello():
    print("world")
```

Another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph",
                '```\ndef hello():\n    print("world")\n```',
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Heading

Paragraph with **bold** text.

> A blockquote
> Multiple lines

1. Ordered list
2. Second item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph with **bold** text.",
                "> A blockquote\n> Multiple lines",
                "1. Ordered list\n2. Second item",
            ],
        )


if __name__ == "__main__":
    unittest.main()
