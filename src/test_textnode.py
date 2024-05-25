import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_noteq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a different text node", text_type=TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_noteq_test_type(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a text node", text_type=TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_urlnoteq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.BOLD, url=None)
        node2 = TextNode(
            text="This is a different text node",
            text_type=TextType.BOLD,
            url="http://boot.dev",
        )
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
