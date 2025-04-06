from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    headings = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    if markdown.startswith(headings):
        return BlockType.HEADING
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    lines = markdown.split("\n")
    
    quote = True
    for line in lines:
        if not line.startswith(">"):
            quote = False

    if quote:
        return BlockType.QUOTE

    unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            unordered_list = False

    if unordered_list:
        return BlockType.UNORDERED_LIST

    ordered_list = True
    i = 1
    for line in lines:    
        if not line.startswith(f"{i}. "):
            ordered_list = False
        i += 1

    if ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

