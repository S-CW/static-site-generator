import unittest

from markdown_block import BlockType, block_to_block_type, markdown_to_block


class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
    def markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
    
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING.value)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE.value)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE.value)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST.value)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST.value)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH.value)