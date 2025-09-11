import unittest

from blocknode import BlockType
from nodeutilities import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title,
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
        ol = """1. This is the first list item in a list block
11. This is a list item
111. This is another list item"""
        quote = """> this is a multiline
> quote"""

        actual_heading_type = block_to_block_type(heading)
        self.assertEqual(BlockType.HEADING, actual_heading_type)

        actual_paragraph_type = block_to_block_type(paragraph)
        self.assertEqual(BlockType.PARAGRAPH, actual_paragraph_type)

        actual_ul_type = block_to_block_type(ul)
        self.assertEqual(BlockType.UNORDERED_LIST, actual_ul_type)

        actual_ol_type = block_to_block_type(ol)
        self.assertEqual(BlockType.ORDERED_LIST, actual_ol_type)

        actual_quote_type = block_to_block_type(quote)
        self.assertEqual(BlockType.QUOTE, actual_quote_type)


class TestMarkDownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and ```code``` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_with_whitespace(self):
        markdown = "  #   Hello World  "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_multiline(self):
        markdown = """# My Title
This is some content
## Subtitle
More content"""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_extract_title_with_other_headers(self):
        markdown = """## This is h2
# This is h1
### This is h3"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is h1")


    def test_extract_title_empty_title(self):
        markdown = "# "
        result = extract_title(markdown)
        self.assertEqual(result, "")

    def test_extract_title_no_h1(self):
        markdown = """## This is h2
### This is h3
Some content"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_only_whitespace(self):
        markdown = "   \n  \n  "
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_multiple_h1_returns_first(self):
        markdown = """# First Title
# Second Title
# Third Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_extract_title_with_special_characters(self):
        markdown = "# Hello, World! @#$%^&*()"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello, World! @#$%^&*()")


if __name__ == "__main__":
    unittest.main()
