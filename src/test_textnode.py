import unittest

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


if __name__ == "__main__":
    unittest.main()
