import unittest

from leafnode import LeafNode
from parentnode import ParentNode

"""    def __init__(self, tag: str, value: str, props: dict | None = None):"""


class TestParentNode(unittest.TestCase):
    def test_tag_value_eq(self):
        node = ParentNode("body", [LeafNode("p", "Some Paragraph Element")])
        node2 = ParentNode("body", [LeafNode("p", "Some Paragraph Element")])
        self.assertEqual(node, node2)

    def test_all_eq(self):
        node = ParentNode(
            "body", [LeafNode("p", "Some Paragraph Element")], {"class": "body"}
        )
        node2 = ParentNode(
            "body", [LeafNode("p", "Some Paragraph Element")], {"class": "body"}
        )
        self.assertEqual(node, node2)

    def test_tag_neq(self):
        node = ParentNode("body", [LeafNode("p", "Some Paragraph Element")])
        node2 = ParentNode("div", [LeafNode("p", "Some Paragraph Element")])
        self.assertNotEqual(node, node2)

    def test_children_neq(self):
        node = ParentNode("body", [LeafNode("p", "Some Paragraph Element")])
        node2 = ParentNode("body", [LeafNode("span", "Some Paragraph Element")])
        self.assertNotEqual(node, node2)

    def test_props_neq(self):
        node = ParentNode(
            "body", [LeafNode("p", "Some Paragraph Element")], {"class": "body"}
        )
        node2 = ParentNode(
            "body", [LeafNode("p", "Some Paragraph Element")], {"id": "content"}
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
