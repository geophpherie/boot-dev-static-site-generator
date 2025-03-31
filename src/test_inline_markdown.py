import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextNodeDelimiter, TextType


class TestNodeSplit(unittest.TestCase):
    def test_two_word_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], TextNodeDelimiter.CODE, TextType.CODE)

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_word_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        result = split_nodes_delimiter([node], TextNodeDelimiter.BOLD, TextType.BOLD)

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_word_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        result = split_nodes_delimiter(
            [node], TextNodeDelimiter.ITALIC, TextType.ITALIC
        )

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_bold_italic_mix_error(self):
        node = TextNode("This is text with a **italic error block_ word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextNodeDelimiter.BOLD, TextType.ITALIC)

    def test_italic_bold_mix_no_error(self):
        node = TextNode("This is text with a **italic error block_ word", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextNodeDelimiter.ITALIC, TextType.ITALIC)

    def test_single_word(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], TextNodeDelimiter.BOLD, TextType.BOLD)

        expected_result = [
            TextNode("bold", TextType.BOLD),
        ]

        self.assertListEqual(result, expected_result)

    def test_double_delims(self):
        node = TextNode(
            "This is text with one **bold word** and another **bold word**.",
            TextType.TEXT,
        )
        result = split_nodes_delimiter([node], TextNodeDelimiter.BOLD, TextType.BOLD)

        expected_result = [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        result = extract_markdown_images(text)

        expected_result = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        ]

        self.assertListEqual(result, expected_result)

    def test_multiple_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)

        expected_result = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]

        self.assertListEqual(result, expected_result)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_double_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        result = extract_markdown_links(text)

        expected_result = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]

        self.assertListEqual(result, expected_result)


class TextSplitImages(unittest.TestCase):
    def test_no_images(self):
        text = TextNode("This is text with no images.", TextType.TEXT)

        result = split_nodes_image([text])

        expected_result = [TextNode("This is text with no images.", TextType.TEXT)]

        self.assertListEqual(result, expected_result)

    def test_one_image_middle(self):
        text = TextNode(
            "This is text with an ![imageA](imageA.png) image in the middle",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(" image in the middle", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_one_image_end(self):
        text = TextNode(
            "This is text with an image at the end ![imageA](imageA.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode("This is text with an image at the end ", TextType.TEXT),
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
        ]

        self.assertListEqual(result, expected_result)

    def test_one_image_start(self):
        text = TextNode(
            "![imageA](imageA.png) This is text with an image at the start",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(" This is text with an image at the start", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_images_middle(self):
        text = TextNode(
            "This is text with two ![imageA](imageA.png) images ![imageB](imageB.png) in it",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(" images ", TextType.TEXT),
            TextNode(
                "imageB",
                TextType.IMAGE,
                "imageB.png",
            ),
            TextNode(" in it", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_images_one_start(self):
        text = TextNode(
            "![imageA](imageA.png) this is text that starts with one image ![imageB](imageB.png) and is followed by another",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(" this is text that starts with one image ", TextType.TEXT),
            TextNode(
                "imageB",
                TextType.IMAGE,
                "imageB.png",
            ),
            TextNode(" and is followed by another", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_images_one_last(self):
        text = TextNode(
            "This is text with two ![imageA](imageA.png) images in it that ends with one ![imageB](imageB.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(" images in it that ends with one ", TextType.TEXT),
            TextNode(
                "imageB",
                TextType.IMAGE,
                "imageB.png",
            ),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_images_one_start_one_last(self):
        text = TextNode(
            "![imageA](imageA.png) This is text that starts with one image and ends with another ![imageB](imageB.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([text])

        expected_result = [
            TextNode(
                "imageA",
                TextType.IMAGE,
                "imageA.png",
            ),
            TextNode(
                " This is text that starts with one image and ends with another ",
                TextType.TEXT,
            ),
            TextNode(
                "imageB",
                TextType.IMAGE,
                "imageB.png",
            ),
        ]

        self.assertListEqual(result, expected_result)


class TextSplitLinks(unittest.TestCase):
    def test_no_links(self):
        text = TextNode("This is text with no links.", TextType.TEXT)

        result = split_nodes_link([text])

        expected_result = [TextNode("This is text with no links.", TextType.TEXT)]

        self.assertListEqual(result, expected_result)

    def test_one_link_middle(self):
        text = TextNode(
            "This is text with an [linkA](linkA.com) link in the middle",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(" link in the middle", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_one_link_end(self):
        text = TextNode(
            "This is text with a link at the end [linkA](linkA.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode("This is text with a link at the end ", TextType.TEXT),
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
        ]

        self.assertListEqual(result, expected_result)

    def test_one_link_start(self):
        text = TextNode(
            "[linkA](linkA.com) This is text with a link at the start",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(" This is text with a link at the start", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_links_middle(self):
        text = TextNode(
            "This is text with two [linkA](linkA.com) links [linkB](linkB.com) in it",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(" links ", TextType.TEXT),
            TextNode(
                "linkB",
                TextType.LINK,
                "linkB.com",
            ),
            TextNode(" in it", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_links_one_start(self):
        text = TextNode(
            "[linkA](linkA.com) this is text that starts with one link [linkB](linkB.com) and is followed by another",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(" this is text that starts with one link ", TextType.TEXT),
            TextNode(
                "linkB",
                TextType.LINK,
                "linkB.com",
            ),
            TextNode(" and is followed by another", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_links_one_last(self):
        text = TextNode(
            "This is text with two [linkA](linkA.com) links in it that ends with one [linkB](linkB.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(" links in it that ends with one ", TextType.TEXT),
            TextNode(
                "linkB",
                TextType.LINK,
                "linkB.com",
            ),
        ]

        self.assertListEqual(result, expected_result)

    def test_two_links_one_start_one_last(self):
        text = TextNode(
            "[linkA](linkA.com) This is text that starts with one link and ends with another [linkB](linkB.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([text])

        expected_result = [
            TextNode(
                "linkA",
                TextType.LINK,
                "linkA.com",
            ),
            TextNode(
                " This is text that starts with one link and ends with another ",
                TextType.TEXT,
            ),
            TextNode(
                "linkB",
                TextType.LINK,
                "linkB.com",
            ),
        ]

        self.assertListEqual(result, expected_result)


class TestTextToTextNode(unittest.TestCase):
    def test_all_types_once(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/courseassets/zjjcJKZ.png) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/courseassets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(result, expected_result)

    def test_some_multiple(self):
        text = "This is **text** with an _italic_ word **words and words** and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/courseassets/zjjcJKZ.png) and a [link](https://boot.dev) and the same link again [link](https://boot.dev) and `das code`"

        result = text_to_textnodes(text)

        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word ", TextType.TEXT),
            TextNode("words and words", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/courseassets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and the same link again ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("das code", TextType.CODE),
        ]

        self.assertListEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
