import unittest

from htmlnode import HTMLNode

"""self.tag = tag
self.value = value
self.children = children
self.props = props"""


class TestHTMLNode(unittest.TestCase):
    def test_tag_eq(self):
        # Equal
        node = HTMLNode("h1")
        node2 = HTMLNode("h1")
        self.assertEqual(node, node2)

    def test_value_eq(self):
        # Equal
        node = HTMLNode(value="This is an html node")
        node2 = HTMLNode(value="This is an html node")
        self.assertEqual(node, node2)

    def test_children_eq(self):
        # All Different
        node = HTMLNode(children=[HTMLNode("This is a text node")])
        node2 = HTMLNode(children=[HTMLNode("This is a text node")])
        self.assertEqual(node, node2)

    def test_props_eq(self):
        # All Different
        node = HTMLNode(props={"class": "body"})
        node2 = HTMLNode(props={"class": "body"})
        self.assertEqual(node, node2)

    def test_all_eq(self):
        # All Different
        node = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        node2 = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        self.assertEqual(node, node2)

    def test_tag_neq(self):
        # All Different
        node = HTMLNode(
            "body",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        node2 = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        self.assertNotEqual(node, node2)

    def test_value_neq(self):
        # All Different
        node = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        node2 = HTMLNode(
            "p",
            "This is a different html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        self.assertNotEqual(node, node2)

    def test_children_neq(self):
        # All Different
        node = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a different child node")],
            {"class": "body"},
        )
        node2 = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text child node")],
            {"class": "body"},
        )
        self.assertNotEqual(node, node2)

    def test_props_neq(self):
        # All Different
        node = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"class": "body"},
        )
        node2 = HTMLNode(
            "p",
            "This is an html node",
            [HTMLNode("This is a text node")],
            {"id": "content"},
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
