import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(text="This is a text node", text_type="bold")
        node2 = TextNode(text="This is a text node", text_type="bold")
        self.assertEqual(node1, node2)

    def test_noteq(self):
        node1 = TextNode(text="This is a text node", text_type="bold")
        node2 = TextNode(text="This is a different text node", text_type="bold")
        self.assertNotEqual(node1, node2)

    def test_noteq_test_type(self):
        node1 = TextNode(text="This is a text node", text_type="bold")
        node2 = TextNode(text="This is a text node", text_type="italic")
        self.assertNotEqual(node1, node2)

    def test_urlnoteq(self):
        node1 = TextNode(text="This is a text node", text_type="bold", url=None)
        node2 = TextNode(
            text="This is a different text node",
            text_type="bold",
            url="http://boot.dev",
        )
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
