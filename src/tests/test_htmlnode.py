import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click here",
            None,
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_single_prop(self):
        node = HTMLNode("p", "Paragraph text", None, {"class": "text-bold"})
        self.assertEqual(node.props_to_html(), ' class="text-bold"')

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Paragraph text", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("div", "Content", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "HTMLNode('p', 'Hello', None, {'class': 'greeting'})"
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
