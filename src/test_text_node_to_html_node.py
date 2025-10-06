import unittest
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node, LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Plain text")
        self.assertEqual(html_node.to_html(), "Plain text")

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_type_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_type_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        self.assertEqual(html_node.to_html(),
                         '<a href="https://www.example.com">Click here</a>')

    def test_text_type_image(self):
        node = TextNode("Image description", TextType.IMAGE,
                        "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
                         "src": "https://www.example.com/image.png", "alt": "Image description"})
        self.assertEqual(html_node.to_html(
        ), '<img src="https://www.example.com/image.png" alt="Image description"></img>')

    def test_invalid_text_type(self):
        node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Invalid text type", str(context.exception))


if __name__ == "__main__":
    unittest.main()
