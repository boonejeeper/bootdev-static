import unittest

from leafnode import LeafNode

"""    def __init__(self, tag: str, value: str, props: dict | None = None):"""


class TestLeafNode(unittest.TestCase):
    def test_tag_value_eq(self):
        node = LeafNode("h1", "Some Heading")
        node2 = LeafNode("h1", "Some Heading")
        self.assertEqual(node, node2)

    def test_all_eq(self):
        node = LeafNode("h1", "Some Heading", {"class": "body"})
        node2 = LeafNode("h1", "Some Heading", {"class": "body"})
        self.assertEqual(node, node2)

    def test_tag_neq(self):
        node = LeafNode("h1", "Some Heading", {"class": "body"})
        node2 = LeafNode("h2", "Some Heading", {"class": "body"})
        self.assertNotEqual(node, node2)

    def test_value_neq(self):
        node = LeafNode("h1", "Some Heading", {"class": "body"})
        node2 = LeafNode("h1", "Some Other Heading", {"class": "body"})
        self.assertNotEqual(node, node2)

    def test_props_neq(self):
        node = LeafNode("h1", "Some Heading", {"class": "body"})
        node2 = LeafNode("h1", "Some Heading", {"id": "content"})
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
