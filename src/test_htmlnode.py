import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        node = HTMLNode(
            props={"href": "http://www.google.com", "target": "_blank"},
        )

        expected_string = ' href="http://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_string)


class TestLeafNode(unittest.TestCase):
    def test_p(self):
        node = LeafNode("p", "This is a paragraph of text.")

        expected_html = "<p>This is a paragraph of text.</p>"

        self.assertEqual(node.to_html(), expected_html)

    def test_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        expected_html = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "value text", None)

        self.assertEqual(node.to_html(), "value text")


class TestParentNode(unittest.TestCase):
    def test_nested_formatting(self):
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

    def test_nested_nested_formatting(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        if node.children is None:
            self.fail()

        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                *node.children,
            ],
        )
        self.assertEqual(
            node2.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
