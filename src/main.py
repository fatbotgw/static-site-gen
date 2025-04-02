from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


def main():
    # text = "This is some text"
    # text_type = TextType.LINK
    # url = "https://www.boot.dev"
    # test_node = TextNode(text, text_type, url)
    # print(test_node)

    # node = TextNode("This is text with a `code block` word", TextType.PLAIN)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    # print(new_nodes)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]


if __name__ == "__main__":
    main()
