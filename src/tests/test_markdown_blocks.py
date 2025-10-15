import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(
            blocks[1],
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        )
        self.assertEqual(blocks[2], "* This is a list item\n* This is another list item")

    def test_markdown_to_blocks_multiple_newlines(self):
        markdown = """Block 1


Block 2



Block 3"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "Block 1")
        self.assertEqual(blocks[1], "Block 2")
        self.assertEqual(blocks[2], "Block 3")


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), "code")

    def test_quote(self):
        self.assertEqual(block_to_block_type(">quote\n>more quote"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph"), "paragraph")


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_multiple_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_unordered_list(self):
        md = """* Item 1
* Item 2
* Item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_quote(self):
        md = """>This is a quote
>spanning multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nspanning multiple lines</blockquote></div>"
        )

    def test_complex_markdown(self):
        md = """# Welcome

This is a **bold** statement with *italic* text.

## Features

* Feature one with `code`
* Feature two with [a link](https://example.com)

```
def hello():
    print("world")
```

>Remember to check the docs!"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Just verify it produces HTML without errors
        self.assertIn("<h1>Welcome</h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn('<a href="https://example.com">a link</a>', html)
        self.assertIn("<pre><code>", html)
        self.assertIn("<blockquote>", html)


if __name__ == "__main__":
    unittest.main()
