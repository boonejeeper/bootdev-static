import unittest

from nodeutilities import (
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


if __name__ == "__main__":
    unittest.main()
