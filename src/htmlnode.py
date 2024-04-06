from typing import Type


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
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"

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
