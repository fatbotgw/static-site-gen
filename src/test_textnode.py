import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def url_none(self):
        node = TextNode("test node", TextType.LINK)
        node2 = TextNode("test node", TextType.LINK, None)
        self.assertEqual(node, node2)

    def diff_type(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("test node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def diff_type2(self):
        node = TextNode("test node", TextType.IMAGE, "https://boot.dev")
        node2 = TextNode("test node", TextType.IMAGE, None)
        self.assertNotEqual(node, node2)




if __name__ == "__main__":
    unittest.main()
