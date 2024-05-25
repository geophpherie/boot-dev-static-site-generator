import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    block_to_html_node,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_three_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""

        result = markdown_to_blocks(markdown)

        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(result, expected_result)

    def test_three_blocks_extra_lines(self):
        markdown = """
# This is a heading





This is a paragraph of text. It has some **bold** and *italic* words inside of it.





* This is a list item
* This is another list item
"""

        result = markdown_to_blocks(markdown)

        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(result, expected_result)

    def test_three_blocks_group(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        result = markdown_to_blocks(markdown)

        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]

        self.assertListEqual(result, expected_result)


class TestBlockToBlockType(unittest.TestCase):
    def test_h1(self):
        markdown_block = "# This is a h1 heading"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.HEADING

        self.assertEqual(result, expected_result)

    def test_h6(self):
        markdown_block = "###### This is a h6 heading"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.HEADING

        self.assertEqual(result, expected_result)

    def test_not_h2(self):
        markdown_block = "##This is not a h2 heading so it should be a paragraph"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_code(self):
        markdown_block = "``` this is a code block ```"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.CODE

        self.assertEqual(result, expected_result)

    def test_code_multiline(self):
        markdown_block = "```python\n this is a\nmultiline\n code block\n ```"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.CODE

        self.assertEqual(result, expected_result)

    def test_not_code(self):
        markdown_block = "``` this is a bad code block ``"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_quote(self):
        markdown_block = "> this is a quote"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.QUOTE

        self.assertEqual(result, expected_result)

    def test_quote_multi(self):
        markdown_block = "> this is a quote\n> that spans\n>multiple\n>lines."

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.QUOTE

        self.assertEqual(result, expected_result)

    def test_quote_bad(self):
        markdown_block = "> this is a quote\n> that spans multiple\nlines poorly"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_unordered_list(self):
        markdown_block = "* this is an\n* unordered\n* list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_unordered_list_with_indent(self):
        markdown_block = "* this is an\n* unordered\n* list\n- with an indent"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_unordered_list_bad(self):
        markdown_block = "* this is an\n*unordered\n* bad\n-list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_ordered_list(self):
        markdown_block = "1. this is an\n2. ordered\n3. list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.ORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_ordered_list_bad(self):
        markdown_block = "1. this is an\n1. ordered\n2. list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)


class TestBlockToHTMLNode(unittest.TestCase):
    def test_blockquote(self):
        markdown_block = "> quote"

        result = block_to_html_node(markdown_block, BlockType.QUOTE).to_html()
        expected_result = "<blockquote>quote</blockquote>"

        self.assertEqual(result, expected_result)

    def test_ul(self):
        markdown_block = "* this is an\n* unordered\n* list"

        result = block_to_html_node(markdown_block, BlockType.UNORDERED_LIST).to_html()
        expected_result = "<ul><li>this is an</li><li>unordered</li><li>list</li></ul>"

        self.assertEqual(result, expected_result)

    def test_ol(self):
        markdown_block = "1. this is an\n2. ordered\n3. list"

        result = block_to_html_node(markdown_block, BlockType.ORDERED_LIST).to_html()
        expected_result = "<ol><li>this is an</li><li>ordered</li><li>list</li></ol>"

        self.assertEqual(result, expected_result)

    def test_code(self):
        markdown_block = "```python\n this is a\nmultiline\n code block\n ```"

        result = block_to_html_node(markdown_block, BlockType.CODE).to_html()
        expected_result = (
            "<code><pre>python\n this is a\nmultiline\n code block\n </pre></code>"
        )

        self.assertEqual(result, expected_result)

    def test_paragraph(self):
        markdown_block = "This should be a paragraph."

        result = block_to_html_node(markdown_block, BlockType.PARAGRAPH).to_html()
        expected_result = "<p>This should be a paragraph.</p>"

        self.assertEqual(result, expected_result)

    def test_heading(self):
        markdown_block = "# This is a h1 heading"
        result = block_to_html_node(markdown_block, BlockType.HEADING).to_html()
        expected_result = "<h1>This is a h1 heading</h1>"
        self.assertEqual(result, expected_result)

        markdown_block = "###### This is a h6 heading"
        result = block_to_html_node(markdown_block, BlockType.HEADING).to_html()
        expected_result = "<h6>This is a h6 heading</h6>"
        self.assertEqual(result, expected_result)

        # dont need to check h7 becuase that would get parsed as a paragraph


class TestMarkdownToHtmlNodes(unittest.TestCase):
    def test_empty_md(self):
        markdown = ""
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div></div>"

        self.assertEqual(result, expected_result)

    def test_simple_md(self):
        markdown = "hi"
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><p>hi</p></div>"

        self.assertEqual(result, expected_result)

    def test_blockquote(self):
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        self.assertEqual(result, expected_result)

    def test_paragraphs(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(result, expected_result)

    def test_lists(self):
        markdown = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"

        self.assertEqual(result, expected_result)

    def test_headings(self):
        markdown = """
# this is an h1

this is paragraph text

## this is an h2
"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
        self.assertEqual(result, expected_result)
