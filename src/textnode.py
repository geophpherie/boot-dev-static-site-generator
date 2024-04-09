from typing import Any
from enum import StrEnum


class TextType(StrEnum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


class TextNodeDelimiter(StrEnum):
    bold = "**"
    italic = "*"
    code = "`"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Any) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: TextNodeDelimiter, text_type: TextType
):
    new_nodes = []

    for node in old_nodes:
        if not node.text_type == TextType.text:
            # don't parse non-text any further
            new_nodes.append(node)
            continue

        tokens = node.text.split(" ")

        current_node = []
        need_match = False
        for token in tokens:
            if not need_match and token[: len(delimiter)] == delimiter:
                # we weren't matching, but we encountered the delimiter
                # close up the current node
                if len(current_node) > 0:
                    new_nodes.append(
                        TextNode(" ".join(current_node) + " ", TextType.text)
                    )

                if token.endswith(delimiter):
                    # it's just a single word
                    new_nodes.append(
                        TextNode(token[len(delimiter) : -len(delimiter)], text_type)
                    )

                    # reset
                    need_match = False
                    current_node = []
                else:
                    # start tracking with current token
                    current_node = [token[len(delimiter) :]]

                    # signal we're looking for an end match
                    need_match = True
            elif need_match and token[-len(delimiter) :] == delimiter:
                # we are matching, and we just finished

                # add this token in
                current_node.append(token[: -len(delimiter)])

                # store it
                new_nodes.append(TextNode(" ".join(current_node), text_type))

                # reset
                need_match = False
                current_node = []
            else:
                current_node.append(token)

        ## if can't find match delimiter raise Exception
        if need_match:
            raise Exception(
                "Markdown improperly formatted, ending match could not be found"
            )
        else:
            if current_node:
                new_nodes.append(TextNode(" " + " ".join(current_node), TextType.text))

    return new_nodes
