import unittest

from blocknode import BlockType
from nodeutilities import (
    block_to_block_type,
    markdown_to_blocks,
)
from textnode import TextNode, TextType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_eq(self):
        # Equal
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
            """
        results = markdown_to_blocks(text)
        self.assertEqual(
            results,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                """- This is the first list item in a list block
- This is a list item
- This is another list item""",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        heading = "# This is a heading"
        paragraph = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        ul = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        ol = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        quote = """> this is a multiline
> quote"""

        actual_heading_type = block_to_block_type(heading)
        self.assertEqual(BlockType.HEADING, actual_heading_type)


if __name__ == "__main__":
    unittest.main()
