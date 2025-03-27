import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # Text tests
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("different text", TextType.IMAGE, "https://boot.dev")
        node2 = TextNode("test node", TextType.IMAGE, "https://boot.dev")
        self.assertNotEqual(node, node2)

    # TextType tests
    def test_diff_type(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("test node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    # URL tests
    def test_link_without_url_raises_exception(self):
        with self.assertRaises(Exception):
            node = TextNode("test node", TextType.LINK)

    def test_url_none(self):
        node = TextNode("test node", TextType.PLAIN)
        node2 = TextNode("test node", TextType.PLAIN, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("test node", TextType.IMAGE, "https://boot.dev")
        node2 = TextNode("test node", TextType.IMAGE, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("text", TextType.IMAGE, "https://boot.dev")
        node2 = TextNode("text", TextType.IMAGE, "https://boot.dev")
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
