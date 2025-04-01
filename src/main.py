from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node, split_nodes_delimiter


def main():
    # text = "This is some text"
    # text_type = TextType.LINK
    # url = "https://www.boot.dev"
    # test_node = TextNode(text, text_type, url)
    # print(test_node)

    # node = TextNode("This is text with a `code block` word", TextType.PLAIN)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    # print(new_nodes)

if __name__ == "__main__":
    main()
