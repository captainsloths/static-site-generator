class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        html_attrs = []
        for key, value in self.props.items():
            html_attrs.append(f'{key}="{value}"')

        return " " + " ".join(html_attrs) if html_attrs else ""

    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNode objects must have a tag value")

        if self.children is None:
            raise ValueError("All ParentNode children must be defined")

        html = ""
        for child in self.children:
            html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
