class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # A string, the HTML tag name
        self.value = value          # A string, the value of the HTML tag
        self.children = children    # List of HTMLNode objects, the children of this node
        self.props = props          # Dictionary, the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        html_attri = ""

        for attribute in self.props:
            html_attri += f' {attribute}="{self.props[attribute]}"'

        return html_attri

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
