from enum import StrEnum, auto

from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(StrEnum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown: str):
    blocks = [part.strip() for part in markdown.split("\n\n") if part != ""]

    return blocks


def markdown_to_html_node(markdown: str):
    children = []
    # parse markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # parse blocks into HTML
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)

    # return html str
    return ParentNode(tag="div", children=children)


def block_to_block_type(markdown_block: str) -> BlockType:
    if _check_if_heading(markdown_block):
        return BlockType.HEADING
    elif _check_if_code_block(markdown_block):
        return BlockType.CODE
    elif _check_if_quote_block(markdown_block):
        return BlockType.QUOTE
    elif _check_if_unordered_list_block(markdown_block):
        return BlockType.UNORDERED_LIST
    elif _check_if_ordered_list_block(markdown_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_html_node(text: str, type: BlockType) -> HTMLNode:
    match type:
        case BlockType.QUOTE:
            return _quote_block_to_html_node(text)
        case BlockType.UNORDERED_LIST:
            return _ul_block_to_html_node(text)
        case BlockType.ORDERED_LIST:
            return _ol_block_to_html_node(text)
        case BlockType.CODE:
            return _code_block_to_html_node(text)
        case BlockType.HEADING:
            return _heading_block_to_html_node(text)
        case BlockType.PARAGRAPH:
            return _paragraph_block_to_html_node(text)
        case _:
            raise Exception(f"Unknown BlockType {type}")


def text_to_html_node(text: str) -> list[LeafNode]:
    # take text and make it into leaf nodes (children of parent)
    # text nodes are our intermediate representation
    text_nodes = text_to_textnodes(text)

    # this is the actual html represetnation
    children = [text_node_to_html_node(node) for node in text_nodes]

    return children


def _paragraph_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    text = ""
    for line in markdown.split("\n"):
        text += " " + line

    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(text.strip())
    return ParentNode(tag="p", children=children)


def _check_if_heading(text: str) -> bool:
    # first char should be a #, then after all # should be a space
    if text.startswith("#") and text.strip("#")[0] == " ":
        parts = text.split()
        heading_num = len(parts[0])
        return 1 <= heading_num < 7

    return False


def _heading_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    heading_parts = markdown.split()
    heading, heading_text = heading_parts[0], " ".join(heading_parts[1:])
    heading_num = len(heading)
    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(heading_text)
    return ParentNode(tag=f"h{heading_num}", children=children)


def _check_if_code_block(text: str) -> bool:
    # first and last line should start with 3 back ticks
    return text[:3] == "```" and text[-3:] == "```"


def _code_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    text = markdown.strip("```")
    children = text_to_html_node(text)
    list_elements.append(ParentNode("pre", children))

    return ParentNode(tag="code", children=list_elements)


def _check_if_quote_block(text: str) -> bool:
    parts = text.split("\n")
    for part in parts:
        if part[0] != ">":
            return False
    return True


def _quote_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    text = ""
    for line in markdown.split("\n"):
        text += line.strip().strip(">")

    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(text.strip())
    return ParentNode(tag="blockquote", children=children)


def _check_if_unordered_list_block(text: str) -> bool:
    parts = text.split("\n")
    for part in parts:
        if part[0] not in ["*", "-"] or part[1] != " ":
            return False
    return True


def _ul_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    for line in markdown.split("\n"):
        # we know it's a ul, so assume it's the correct format
        children = text_to_html_node(line[2:])
        list_elements.append(ParentNode("li", children))

    return ParentNode(tag="ul", children=list_elements)


def _check_if_ordered_list_block(text: str) -> bool:
    parts = text.split("\n")
    for i, part in enumerate(parts, 1):
        if not part[0].isnumeric() or part[1] != "." or part[0] != str(i):
            return False
    return True


def _ol_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    for line in markdown.split("\n"):
        # we know it's a ol, so assume it's the correct format
        children = text_to_html_node(line[3:])
        list_elements.append(ParentNode("li", children))

    return ParentNode(tag="ol", children=list_elements)
