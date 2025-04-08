import re

from htmlnode import LeafNode, HTMLNode, ParentNode
import htmlnode
from textnode import TextNode, TextType
from block_type import BlockType, block_to_block_type


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
            raise ValueError(f"Unclosed delimiter '{delimiter}' in text: {node.text}")

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

# This is my version, written based on the unit test provided in the assignment
# which seems to have had extra indenting in the markdown.  This is why there
# is an extra for loop and adittional split/join that removes the extra indents
#
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

# This version is from the assignment solution, but won't work if the markdown
# has extra indentions in the unit test, see test_converters.py for examples
#
# def markdown_to_blocks(markdown):
#     blocks = markdown.split("\n\n")
#     filtered_blocks = []
#     for block in blocks:
#         if block == "":
#             continue
#         block = block.strip()
#         filtered_blocks.append(block)
#     return filtered_blocks

def block_to_html(node_list, block_type):
    html_node_list = []
    for node in node_list:
        html_node_list.append(text_node_to_html_node(node))

    # block_type_to_tag = {
    #     BlockType.PARAGRAPH: "p",
    #     BlockType.QUOTE: "blockquote",
    #     BlockType.CODE: "pre",
    #     BlockType.HEADING: "h",
    #     BlockType.UNORDERED_LIST: "ul",
    #     BlockType.ORDERED_LIST: "ol"
    # }

    if block_type is BlockType.PARAGRAPH:
        return ParentNode("p", html_node_list)
    elif block_type is BlockType.CODE:
        return ParentNode("pre", html_node_list)
    elif block_type is BlockType.QUOTE:
        return ParentNode("blockquote", html_node_list)
    elif block_type is BlockType.HEADING:
        pass
    elif block_type is BlockType.UNORDERED_LIST:
        pass
    elif block_type is BlockType.ORDERED_LIST:
        pass
    else:
        raise Exception(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    html_node_list = []

    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type is BlockType.CODE:
            block_content = block[3:-3].lstrip("\n")
            new_node = TextNode(block_content, TextType.CODE)
            html_node = block_to_html([new_node], block_type)
        else:
            block = block.replace("\n", " ")

            if block_type is BlockType.QUOTE:
                block = block.replace("> ", "")
            # print(f"\n***block:\n{block} \n***type: {block_type}")
            html_node = block_to_html(text_to_textnodes(block), block_type)
            
        html_node_list.append(html_node)
    
    html_node = ParentNode("div", html_node_list)
    # print(f"\n***return value:\n{html_node.to_html()}")
    return html_node
