import re

from textnode import TextNode, TextNodeDelimiter, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: TextNodeDelimiter, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            # don't parse non-text any further
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # this is an even split aka missing an ending
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")

        for index, part in enumerate(parts):
            # this is empty, nothing to add
            if part == "":
                continue
            elif index % 2 == 0:
                # when we split, the even numbers are just texts
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        # no images found
        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        # some images found
        for i, image in enumerate(images, 1):
            parts = text.split(f"![{image[0]}]({image[1]})", 1)

            if parts[0] == "":
                # image is first
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            elif parts[1] == "":
                # image is last
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                # image is in the middle
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # second part might need split
            # if this is the last image add in the part, other wise the part needs split again
            if i == len(images) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        # no links found
        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        # some links found
        for i, link in enumerate(links, 1):
            parts = text.split(f"[{link[0]}]({link[1]})", 1)

            if parts[0] == "":
                # link is first
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            elif parts[1] == "":
                # link is last
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                # link is in the middle
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # second part might need split
            # if this is the last link add in the part, other wise the part needs split again
            if i == len(links) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]

    return new_nodes


def extract_markdown_images(text: str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return matches


def extract_markdown_links(text: str):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    return matches


def text_to_textnodes(text: str):
    nodes = split_nodes_delimiter(
        old_nodes=[TextNode(text, TextType.TEXT)],
        delimiter=TextNodeDelimiter.BOLD,
        text_type=TextType.BOLD,
    )

    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter=TextNodeDelimiter.ITALIC,
        text_type=TextType.ITALIC,
    )

    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter=TextNodeDelimiter.CODE,
        text_type=TextType.CODE,
    )

    nodes = split_nodes_image(old_nodes=nodes)
    nodes = split_nodes_link(old_nodes=nodes)

    return nodes
