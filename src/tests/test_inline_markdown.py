import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_code_blocks(self):
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_starting_with_delimiter(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ending_with_delimiter(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_entire_text_delimited(self):
        node = TextNode("`entire text`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("entire text", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter_raises_error(self):
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("First `code` text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("Second `block` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("Second ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_delimited_text(self):
        node = TextNode("Text with `` empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_consecutive_delimiters(self):
        node = TextNode("`code1``code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_image_with_empty_alt(self):
        text = "Image with empty alt ![](https://i.imgur.com/test.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/test.png")], matches)

    def test_extract_image_ignores_links(self):
        text = "A [link](https://example.com) and ![image](https://i.imgur.com/test.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/test.png")], matches)

    def test_extract_consecutive_images(self):
        text = "![first](url1.png)![second](url2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "url1.png"), ("second", "url2.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_single_link(self):
        text = "Click [here](https://www.example.com) to visit"
        matches = extract_markdown_links(text)
        self.assertListEqual([("here", "https://www.example.com")], matches)

    def test_extract_no_links(self):
        text = "This text has no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_link_with_empty_text(self):
        text = "Empty link text [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_links_ignores_images(self):
        text = "A ![image](https://i.imgur.com/test.png) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_consecutive_links(self):
        text = "[first](url1.com)[second](url2.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("first", "url1.com"), ("second", "url2.com")], matches)

    def test_extract_mixed_images_and_links(self):
        text = "[link1](url1) ![img](imgurl) [link2](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "Text ending with ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("Just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Just plain text with no images", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_consecutive_images(self):
        node = TextNode(
            "![first](url1.png)![second](url2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1.png"),
                TextNode("second", TextType.IMAGE, "url2.png"),
            ],
            new_nodes,
        )

    def test_split_image_with_empty_alt(self):
        node = TextNode(
            "Image with ![](https://i.imgur.com/test.png) empty alt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/test.png"),
                TextNode(" empty alt", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](url1.png) text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("Second ![img2](url2.png) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode(" text", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("Second ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_three_images(self):
        node = TextNode(
            "![one](url1) middle ![two](url2) end ![three](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" end ", TextType.TEXT),
                TextNode("three", TextType.IMAGE, "url3"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://www.example.com) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Text ending with [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("Just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Just plain text with no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_consecutive_links(self):
        node = TextNode(
            "[first](url1.com)[second](url2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1.com"),
                TextNode("second", TextType.LINK, "url2.com"),
            ],
            new_nodes,
        )

    def test_split_link_with_empty_text(self):
        node = TextNode(
            "Link with [](https://example.com) empty text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_non_text_node_unchanged(self):
        node = TextNode("already code", TextType.CODE)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("already code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](url1) text", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
            TextNode("Second [link2](url2) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" text", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
                TextNode("Second ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_three_links(self):
        node = TextNode(
            "[one](url1) middle [two](url2) end [three](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.LINK, "url2"),
                TextNode(" end ", TextType.TEXT),
                TextNode("three", TextType.LINK, "url3"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "A ![image](img.png) and [link](url.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ![image](img.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is just plain text with no formatting", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_italic_only(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_code_only(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_only(self):
        text = "This is an ![image](https://example.com/img.png) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_link_only(self):
        text = "This is a [link](https://example.com) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_types(self):
        text = "**Bold** and *italic* and `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_consecutive_formatting(self):
        text = "**bold***italic*`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_mixed_images_and_links(self):
        text = "Check ![img](img.png) and [link](url.com) out"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" out", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
