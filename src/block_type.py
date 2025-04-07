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

    if markdown.startswith(">"):    
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if markdown.startswith("1. "):
        i = 1
        for line in lines:    
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

