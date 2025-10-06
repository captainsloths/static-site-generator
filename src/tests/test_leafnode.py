import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode(
            "a", "Link", {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.boot.dev" target="_blank">Link</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "An image"})
        self.assertEqual(
            node.to_html(), '<img src="image.png" alt="An image"></img>')


if __name__ == "__main__":
    unittest.main()
