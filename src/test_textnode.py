import unittest

from textnode import TextNode, TextNodeDelimiter, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.bold)
        node2 = TextNode(text="This is a text node", text_type=TextType.bold)
        self.assertEqual(node1, node2)

    def test_noteq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.bold)
        node2 = TextNode(text="This is a different text node", text_type=TextType.bold)
        self.assertNotEqual(node1, node2)

    def test_noteq_test_type(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.bold)
        node2 = TextNode(text="This is a text node", text_type=TextType.italic)
        self.assertNotEqual(node1, node2)

    def test_urlnoteq(self):
        node1 = TextNode(text="This is a text node", text_type=TextType.bold, url=None)
        node2 = TextNode(
            text="This is a different text node",
            text_type=TextType.bold,
            url="http://boot.dev",
        )
        self.assertNotEqual(node1, node2)


class TestNodeSplit(unittest.TestCase):
    def test_two_word_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = split_nodes_delimiter([node], TextNodeDelimiter.code, TextType.code)

        expectedResult = [
            TextNode("This is text with a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" word", TextType.text),
        ]

        self.assertListEqual(new_nodes, expectedResult)

    def test_two_word_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.text)
        new_nodes = split_nodes_delimiter([node], TextNodeDelimiter.bold, TextType.bold)

        expectedResult = [
            TextNode("This is text with a ", TextType.text),
            TextNode("bold block", TextType.bold),
            TextNode(" word", TextType.text),
        ]

        self.assertListEqual(new_nodes, expectedResult)

    def test_two_word_italic(self):
        node = TextNode("This is text with a *italic block* word", TextType.text)
        new_nodes = split_nodes_delimiter(
            [node], TextNodeDelimiter.italic, TextType.italic
        )

        expectedResult = [
            TextNode("This is text with a ", TextType.text),
            TextNode("italic block", TextType.italic),
            TextNode(" word", TextType.text),
        ]

        self.assertListEqual(new_nodes, expectedResult)

    def test_bold_italic_mix_error(self):
        node = TextNode("This is text with a **italic error block* word", TextType.text)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextNodeDelimiter.bold, TextType.italic)

    def test_italic_bold_mix_no_error(self):
        node = TextNode("This is text with a **italic error block* word", TextType.text)
        new_nodes = split_nodes_delimiter(
            [node], TextNodeDelimiter.italic, TextType.italic
        )

        expectedResult = [
            TextNode("This is text with a ", TextType.text),
            TextNode("*italic error block", TextType.italic),
            TextNode(" word", TextType.text),
        ]

        self.assertListEqual(new_nodes, expectedResult)

    def test_single_word(self):
        node = TextNode("**bold**", TextType.text)
        new_nodes = split_nodes_delimiter([node], TextNodeDelimiter.bold, TextType.bold)

        expectedResult = [
            TextNode("bold", TextType.bold),
        ]

        self.assertListEqual(new_nodes, expectedResult)


if __name__ == "__main__":
    unittest.main()
