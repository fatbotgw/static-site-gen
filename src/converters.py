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
    image_list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return image_list


def extract_markdown_links(text):
    image_list = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

    return image_list

def split_nodes_image(old_nodes):
    node_list = []

    for node in old_nodes:
        delimiter_list = extract_markdown_images(node.text)

        if not delimiter_list:
            node_list.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in delimiter_list:
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            # Add a text node for the part before the image (if not empty)
            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.PLAIN))
                
            if alt_text:
                # Add a node for the image itself
                node_list.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # The remaining text becomes what's after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            node_list.append(TextNode(remaining_text, TextType.PLAIN))

    return node_list

def split_nodes_link(old_nodes):
    node_list = []

    for node in old_nodes:
        delimiter_list = extract_markdown_links(node.text)

        if not delimiter_list:
            node_list.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in delimiter_list:
            image_markdown = f"[{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            # Add a text node for the part before the image (if not empty)
            if parts[0]:
                node_list.append(TextNode(parts[0], TextType.PLAIN))
                

            if alt_text:
                # Add a node for the image itself
                node_list.append(TextNode(alt_text, TextType.LINK, url))
            
            # The remaining text becomes what's after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            node_list.append(TextNode(remaining_text, TextType.PLAIN))

    return node_list


def text_to_textnodes(text):
    new_node = TextNode(text, TextType.PLAIN)
    node_list = [new_node]

    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)

    return node_list

def markdown_to_blocks(markdown):
    new_list = markdown.split("\n\n")
    out_list = []
    
    for item in new_list:
        # Strip leading/trailing whitespace
        stripped_item = item.strip()
        # Skip now empty items
        if not stripped_item:
            continue
        
        # Split the block into lines, strip each line, then rejoin
        lines = stripped_item.split("\n")
        lines_out = []
        for line in lines:
            lines_out.append(line.strip())
        
        out_list.append("\n".join(lines_out))

    return out_list