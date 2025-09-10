import re
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown TextNode TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node = node.text.split(delimiter)
        if len(split_node) % 2 != 1:
            return Exception("Unbalanced delimiters")

        current_text_type = TextType.TEXT
        for i in range(0, len(split_node)):
            if i % 2 == 1:
                current_text_type = text_type
            else:
                current_text_type = TextType.TEXT

            new_nodes.append(TextNode(split_node[i], current_text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        sections = []
        node_text = node.text
        for image in images:
            image_alt, image_link = image
            sections = node_text.split(f"![{image_alt}]({image_link})", 1)
            new_nodes.append(TextNode(node_text.text, TextType.TEXT))


def split_nodes_link(old_nodes):
    pass


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
