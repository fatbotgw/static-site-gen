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


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("Leaf nodes must have a value")

        if self.tag is None:
            return f"{self.value}"
        
        if self.props is not None:
            if self.tag == "img":
                return f"<{self.tag}{self.props_to_html()} />"
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Node must have a tag")

        if self.children is None:
            raise ValueError("Not a ParentNode, no children found")

        html_out = f"<{self.tag}>"
        for node in self.children:
            html_out += node.to_html()

        html_out += f"</{self.tag}>"

        return html_out

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

