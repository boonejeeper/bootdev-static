import unittest

from nodeutilities import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    text_node_to_html_node,
)
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_all_neq(self):
        # All Different
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Google", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        # Only different text
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Hello World!", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_neq(self):
        # Only different text_type
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        # Only different url
        node = TextNode("This is a link node", TextType.LINK, "www.microsoft.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.google.com")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestTextNodeSplitDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is **bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            f"{nodes}",
            "[TextNode(This is , text, None), TextNode(bold, bold, None), TextNode(, text, None)]",
        )


class TestTextNodeExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestTextNodeExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
