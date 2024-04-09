from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["LeafNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        html_string = ""
        for k, v in self.props.items():
            html_string += f' {k}="{v}"'

        return html_string


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_str = self.props_to_html()

        open_tag = f"<{self.tag}{props_str}>"
        close_tag = f"</{self.tag}>"

        html_str = f"{open_tag}{self.value}{close_tag}"

        return html_str


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[LeafNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        props_str = self.props_to_html()

        open_tag = f"<{self.tag}{props_str}>"
        close_tag = f"</{self.tag}>"

        html_str = f"{open_tag}"

        for child in self.children:
            html_str += child.to_html()

        html_str += close_tag
        return html_str


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.text:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.bold:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.italic:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.code:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.link:
            if text_node.url is None:
                text_node.url = ""
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.image:
            if text_node.url is None:
                text_node.url = ""
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception(f"Unknown TextNode type {text_node.text_type}")
