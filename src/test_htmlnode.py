import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from converters import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        tag = "href"
        value = "https://www.google.com"
        children = []
        props = {"href": "https://www.google.com","target": "_blank",}

        node = HTMLNode(tag, value, children, props).props_to_html()
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node, node2)

    def test_props_to_html_not_eq(self):
        # <link href="/shared-assets/misc/link-element-example.css" rel="stylesheet" />
        tag = "link"
        value = ""
        children = []
        props = {"href": "/shared-assets/misc/link-element-example.css",
                    "rel": "stylesheet"}
        
        node = HTMLNode(tag, value, children, props).props_to_html()
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertNotEqual(node, node2)


    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a_mult(self):
        node = LeafNode("a", "Link me!", {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev" target="_blank">Link me!</a>')

    def test_leaf_to_html_error(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None).to_html()

    def test_leaf_to_html_specials(self):
        node = LeafNode("p", "    Indented text    ")
        self.assertEqual(node.to_html(), "<p>    Indented text    </p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_to_html_with_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, None).to_html()


if __name__ == "__main__":
    unittest.main()
