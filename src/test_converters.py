import unittest

from converters import (
    split_nodes_delimiter,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
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

    def test_split_backtick(self):
        node = TextNode("This is a `code block` example.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" example.", TextType.PLAIN),
        ]

    def test_split_bold(self):
        node = TextNode("This is a **bold** example.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" example.", TextType.PLAIN),
        ]

    def test_split_italic(self):
        node = TextNode("This is an _italic_ example.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert new_nodes == [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" example.", TextType.PLAIN),
        ]

    def test_split_mismatch_delim(self):
        node = TextNode("This is an _italic example.", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_split_plain(self):
        node = TextNode("This is a plain text example.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is a plain text example.", TextType.PLAIN),
        ]

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_list = extract_markdown_images(text)
        assert new_list == [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

    def test_extract_markdown_image_and_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_list = extract_markdown_images(text)
        assert new_list == [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ]

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        new_list = extract_markdown_links(text)
        assert new_list == [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

    def test_extract_markdown_link_and_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_list = extract_markdown_links(text)
        assert new_list == [
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_tail_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) picture.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" picture.", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_linkss_tail_text(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) picture.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" picture.", TextType.PLAIN),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
