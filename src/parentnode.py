from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or len(self.tag) == 0:
            raise ValueError("tags are required for ParentNodes")

        if self.children is None or len(self.children):
            raise ValueError("children are required for ParentNodes")

        props_string = ""
        if self.props is not None:
            props_string = " " + self.props_to_html()

        child_elements = []
        for child in self.children:
            child_elements.append(child.to_html())

        return f"<{self.tag}{props_string}>{'\n'.join(child_elements)}</{self.tag}>"
