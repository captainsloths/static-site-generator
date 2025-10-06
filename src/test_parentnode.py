import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_nested_parents(self):
        inner_leaf = LeafNode("span", "Hello")
        inner_parent = ParentNode("div", [inner_leaf], {"class": "inner"})
        outer_parent = ParentNode("section", [inner_parent], {"id": "main"})
        self.assertEqual(
            outer_parent.to_html(),
            '<section id="main"><div class="inner"><span>Hello</span></div></section>',
        )

    def test_to_html_many_children(self):
        children = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3"),
        ]
        parent_node = ParentNode("ul", children)
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("tag", str(context.exception).lower())

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("children", str(context.exception).lower())

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_complex_nesting(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        parent1 = ParentNode("p", [leaf1, leaf2])
        leaf3 = LeafNode("span", "Span text")
        parent2 = ParentNode("div", [parent1, leaf3])
        self.assertEqual(
            parent2.to_html(),
            "<div><p><b>Bold</b><i>Italic</i></p><span>Span text</span></div>",
        )


if __name__ == "__main__":
    unittest.main()
