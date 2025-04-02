import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, text_node.url)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("img", "", props)
        case _:
            raise Exception("invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            node_list.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unclose delimiter '{delimiter}' in text: {node.text}")

        inside_delimiter = False
        for part in parts:
            if inside_delimiter:
                node_list.append(TextNode(part, text_type))
            else:
                node_list.append(TextNode(part, TextType.PLAIN))
            inside_delimiter = not inside_delimiter

    return node_list

def extract_markdown_images(text):
    image_list = []

    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)

    for i in range(len(url)):
        image_list.append((alt_text[i], url[i]))
        i += 1

    return image_list


def extract_markdown_links(text):
    image_list = []

    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)

    for i in range(len(url)):
        image_list.append((alt_text[i], url[i]))
        i += 1

    return image_list


