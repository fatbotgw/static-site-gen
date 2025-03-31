import unittest

from converters import text_node_to_html_node
from textnode import TextNode, TextType


class TestConverters(unittest.TestCase):
    def test_text_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_a_tag(self):
        node = TextNode(
            "This is a link",
            TextType.LINK,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(
            html_node.props, {"href": "https://boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://boot.dev" target="_blank">This is a link</a>',
        )

    def test_text_image(self):
        node = TextNode(
            "A majestic bear wizard", TextType.IMAGE, "https://example.com/bear.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["alt"], "A majestic bear wizard")
        self.assertEqual(html_node.props["src"], "https://example.com/bear.png")
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/bear.png" alt="A majestic bear wizard" />',
        )


if __name__ == "__main__":
    unittest.main()
