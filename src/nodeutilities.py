import re
from textnode import TextNode, TextType
from leafnode import LeafNode
from blocknode import BlockType


def markdown_to_blocks(markdown):
    if len(markdown) == 0:
        raise Exception("missing markdown, unable to parse")

    markdown_blocks = markdown.split("\n\n")

    filtered_blocks = []

    for markdown_block in markdown_blocks:
        markdown_block = markdown_block.strip()
        if markdown_block == "":
            continue

        filtered_blocks.append(markdown_block)

    return filtered_blocks


def text_to_textnodes(text):
    new_nodes = []

    node = TextNode(text, TextType.TEXT)
    new_nodes.append(node)

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "```", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # check each line starts with '>'
    is_quote = True
    for line in block.split("\n"):
        if not line.startswith(">"):
            is_quote = False
    if is_quote:
        return BlockType.QUOTE

    # check each line starts iwth '-'
    is_unordered_list = True
    for line in block.split("\n"):
        if not line.startswith("-"):
            is_quote = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # check each line starts with a number followed by '.'
    is_unordered_list = True
    for line in block.split("\n"):
        if not re.search(r"^\d+\.", line):
            is_quote = False
    if is_unordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


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
        if len(split_node) % 2 == 0:
            return Exception("invalid markdown, formatted section not closed")

        current_text_type = TextType.TEXT
        for i in range(0, len(split_node)):
            if i % 2 == 0:
                current_text_type = TextType.TEXT
            else:
                current_text_type = text_type

            if split_node[i] != "":
                new_nodes.append(TextNode(split_node[i], current_text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            # didn't find any images
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            # didn't find any links
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
