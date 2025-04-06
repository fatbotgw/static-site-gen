import unittest
from block_type import BlockType, block_to_block_type

class TestBlockTypeFunction(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        block = "### This is a level 3 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "####### Bad Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote(self):
        block = "> This is a quote\n> It spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> This is not a quote\nIt spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "This is not a quote\n> It spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_invalid_ordered_list(self):
        # Numbers don't start at 1
        block = "2. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)