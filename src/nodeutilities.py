"""
Node utilities for converting markdown to HTML.

This module provides functions for parsing markdown text and converting it into
a tree structure of HTML nodes. It handles various markdown elements including
headers, paragraphs, lists, quotes, links, images, and inline formatting.
"""

import re
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from blocknode import BlockType


def markdown_to_html_node(markdown):
    """
    Convert markdown text to an HTML node tree.
    
    This is the main entry point for markdown to HTML conversion. It processes
    the markdown text by splitting it into blocks, determining block types,
    and converting each block to appropriate HTML nodes.
    
    Args:
        markdown (str): The markdown text to convert.
        
    Returns:
        ParentNode: A div node containing all the converted HTML blocks.
        
    Example:
        markdown = "# Hello\\n\\nThis is **bold** text."
        Returns: ParentNode("div", [heading_node, paragraph_node])
    """
    blocks = markdown_to_blocks(markdown)
    new_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            # Handle headings - determine level and remove # symbols
            heading_level = 0
            for char in block:
                if char == '#':
                    heading_level += 1
                else:
                    break
            
            # Remove the # symbols and whitespace from the heading text
            heading_text = block[heading_level:].strip()
            heading_tag = f"h{min(heading_level, 6)}"  # Cap at h6
            
            children_nodes = text_to_children(heading_text)
            block_node = ParentNode(heading_tag, children_nodes, None)
        elif block_type == BlockType.CODE:
            # Handle code blocks - use <pre><code> structure
            # Remove the ``` markers from the code block
            code_content = block
            if code_content.startswith("```") and code_content.endswith("```"):
                code_content = code_content[3:-3].strip()
            
            # Create a code node with the raw content (no inline processing)
            code_node = LeafNode("code", code_content)
            block_node = ParentNode("pre", [code_node], None)
        elif block_type == BlockType.QUOTE:
            # Handle blockquotes - remove > markers from each line
            quote_lines = []
            for line in block.split('\n'):
                if line.startswith('>'):
                    # Remove the > and any following space
                    quote_content = line[1:].lstrip()
                    quote_lines.append(quote_content)
                else:
                    quote_lines.append(line)
            
            # Join the lines and process as normal text
            quote_text = '\n'.join(quote_lines)
            children_nodes = text_to_children(quote_text)
            block_node = ParentNode("blockquote", children_nodes, None)
        elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
            # Handle lists - wrap each item in <li> tags
            block_tag = tag_for_block_type(block_type)
            list_items = []
            
            for line in block.split('\n'):
                line = line.strip()
                if line:
                    # Remove list markers (- or 1. etc.)
                    if block_type == BlockType.UNORDERED_LIST:
                        item_text = line[1:].strip()  # Remove -
                    else:  # ORDERED_LIST
                        item_text = re.sub(r'^\d+\.\s*', '', line)  # Remove 1. etc.
                    
                    item_children = text_to_children(item_text)
                    list_item = ParentNode("li", item_children, None)
                    list_items.append(list_item)
            
            block_node = ParentNode(block_tag, list_items, None)
        else:
            # Handle other block types normally
            block_tag = tag_for_block_type(block_type)
            children_nodes = text_to_children(block)
            block_node = ParentNode(block_tag, children_nodes, None)
        
        new_nodes.append(block_node)

    parent_node = ParentNode("div", new_nodes, None)
    return parent_node


def text_to_children(text):
    """
    Convert text content to a list of HTML child nodes.
    
    Parses inline markdown formatting (bold, italic, code, links, images)
    and converts each piece to appropriate HTML nodes.
    
    Args:
        text (str): The text content to parse and convert.
        
    Returns:
        list: List of HTMLNode objects representing the parsed content.
        
    Example:
        text = "This is **bold** and _italic_ text."
        Returns: [LeafNode(None, "This is "), LeafNode("b", "bold"), ...]
    """
    children = []
    children_text_nodes = text_to_textnodes(text)
    for child_node in children_text_nodes:
        children.append(text_node_to_html_node(child_node))

    return children


def tag_for_block_type(block_type):
    """
    Get the HTML tag name for a given block type.
    
    Maps BlockType enum values to their corresponding HTML tag names.
    
    Args:
        block_type (BlockType): The type of markdown block.
        
    Returns:
        str: The HTML tag name for the block type.
        
    Example:
        BlockType.HEADING -> "h1"
        BlockType.PARAGRAPH -> "p"
        BlockType.UNORDERED_LIST -> "ul"
    """
    match block_type:
        case BlockType.HEADING:
            return "h1"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case _:
            return "p"


def markdown_to_blocks(markdown):
    """
    Split markdown text into individual blocks.
    
    Separates markdown content into blocks based on double newlines.
    Normalizes whitespace within paragraph blocks while preserving
    formatting for lists and other structured content.
    
    Args:
        markdown (str): The markdown text to split.
        
    Returns:
        list: List of markdown block strings.
        
    Raises:
        Exception: If markdown is empty.
        
    Example:
        markdown = "# Header\\n\\nParagraph text\\n\\n- List item"
        Returns: ["# Header", "Paragraph text", "- List item"]
    """
    if len(markdown) == 0:
        raise Exception("missing markdown, unable to parse")

    markdown_blocks = markdown.split("\n\n")

    filtered_blocks = []

    for markdown_block in markdown_blocks:
        markdown_block = markdown_block.strip()
        if markdown_block == "":
            continue

        # Only normalize whitespace for paragraph blocks (not lists, quotes, etc.)
        block_type = block_to_block_type(markdown_block)
        if block_type == BlockType.PARAGRAPH:
            # Normalize whitespace within paragraphs - replace newlines with spaces
            markdown_block = re.sub(r'\n', ' ', markdown_block)

        filtered_blocks.append(markdown_block)

    return filtered_blocks


def text_to_textnodes(text):
    """
    Parse text content and extract formatted text nodes.
    
    Processes inline markdown formatting by splitting text on delimiters
    and creating TextNode objects for each piece. Handles bold, italic,
    code, links, and images.
    
    Args:
        text (str): The text content to parse.
        
    Returns:
        list: List of TextNode objects representing the parsed content.
        
    Example:
        text = "This is **bold** and _italic_ text."
        Returns: [TextNode("This is ", TEXT), TextNode("bold", BOLD), ...]
    """
    new_nodes = []

    node = TextNode(text, TextType.TEXT)
    new_nodes.append(node)

    # Process different formatting types in order
    # Process single backticks for inline code first (before triple backticks)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "```", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Analyzes the content of a markdown block to determine its type
    based on common markdown patterns.
    
    Args:
        block (str): The markdown block to analyze.
        
    Returns:
        BlockType: The type of the markdown block.
        
    Example:
        "# Header" -> BlockType.HEADING
        "- List item" -> BlockType.UNORDERED_LIST
        "1. Numbered item" -> BlockType.ORDERED_LIST
    """
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for horizontal rule
    if re.match(r'^[-*_]{3,}$', block.strip()):
        return BlockType.PARAGRAPH

    # Check if each line starts with '>' (quote block)
    is_quote = True
    for line in block.split("\n"):
        if not line.startswith(">"):
            is_quote = False
    if is_quote:
        return BlockType.QUOTE

    # Check if each line starts with '-' (unordered list)
    is_unordered_list = True
    for line in block.split("\n"):
        if not line.startswith("-"):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # Check if each line starts with a number followed by '.' (ordered list)
    is_ordered_list = True
    for line in block.split("\n"):
        if not re.search(r"^\d+\.", line):
            is_ordered_list = False
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTML LeafNode.
    
    Maps TextNode types to their corresponding HTML tags and attributes.
    
    Args:
        text_node (TextNode): The TextNode to convert.
        
    Returns:
        LeafNode: The corresponding HTML node.
        
    Raises:
        Exception: If the TextNode type is not recognized.
        
    Example:
        TextNode("bold text", BOLD) -> LeafNode("b", "bold text")
        TextNode("link text", LINK, "http://example.com") -> LeafNode("a", "link text", {"href": "http://example.com"})
    """
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
    """
    Split text nodes on a delimiter and apply formatting to alternating sections.
    
    Processes nodes to find delimiter patterns and creates new TextNodes
    with alternating text types. Used for bold (**), italic (_), and code (```) formatting.
    
    Args:
        old_nodes (list): List of TextNode objects to process.
        delimiter (str): The delimiter to split on (e.g., "**", "_", "```").
        text_type (TextType): The type to apply to delimited sections.
        
    Returns:
        list: List of TextNode objects with formatting applied.
        
    Raises:
        Exception: If a delimiter is not properly closed (odd number of delimiters).
        
    Example:
        nodes = [TextNode("This is **bold** text", TEXT)]
        split_nodes_delimiter(nodes, "**", BOLD)
        Returns: [TextNode("This is ", TEXT), TextNode("bold", BOLD), TextNode(" text", TEXT)]
    """
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
    """
    Extract and convert markdown images to TextNode objects.
    
    Processes text nodes to find markdown image syntax (![alt](url))
    and converts them to IMAGE type TextNodes.
    
    Args:
        old_nodes (list): List of TextNode objects to process.
        
    Returns:
        list: List of TextNode objects with images converted.
        
    Raises:
        ValueError: If an image markdown syntax is malformed.
        
    Example:
        nodes = [TextNode("Here's an image: ![alt](url)", TEXT)]
        split_nodes_image(nodes)
        Returns: [TextNode("Here's an image: ", TEXT), TextNode("alt", IMAGE, "url")]
    """
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
    """
    Extract and convert markdown links to TextNode objects.
    
    Processes text nodes to find markdown link syntax ([text](url))
    and converts them to LINK type TextNodes.
    
    Args:
        old_nodes (list): List of TextNode objects to process.
        
    Returns:
        list: List of TextNode objects with links converted.
        
    Raises:
        ValueError: If a link markdown syntax is malformed.
        
    Example:
        nodes = [TextNode("Here's a [link](url)", TEXT)]
        split_nodes_link(nodes)
        Returns: [TextNode("Here's a ", TEXT), TextNode("link", LINK, "url")]
    """
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
    """
    Extract all markdown images from text using regex.
    
    Finds all instances of markdown image syntax (![alt](url)) in the text
    and returns a list of tuples containing (alt_text, url).
    
    Args:
        text (str): The text to search for images.
        
    Returns:
        list: List of tuples (alt_text, url) for each image found.
        
    Example:
        text = "Here's an ![alt text](image.jpg) image."
        Returns: [("alt text", "image.jpg")]
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """
    Extract all markdown links from text using regex.
    
    Finds all instances of markdown link syntax ([text](url)) in the text
    and returns a list of tuples containing (link_text, url).
    Excludes images by using negative lookbehind.
    
    Args:
        text (str): The text to search for links.
        
    Returns:
        list: List of tuples (link_text, url) for each link found.
        
    Example:
        text = "Here's a [link text](http://example.com) link."
        Returns: [("link text", "http://example.com")]
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown):
    """
    Extract the h1 header from markdown text.
    
    Searches for the first line that starts with '# ' (hash followed by space)
    and returns the title text without the hash and whitespace.
    
    Args:
        markdown (str): The markdown text to extract title from.
        
    Returns:
        str: The title text without the # and whitespace.
        
    Raises:
        Exception: If no h1 header is found.
        
    Example:
        markdown = "# My Title\\n\\nSome content"
        Returns: "My Title"
    """
    lines = markdown.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            # Found h1 header, return the title without the # and whitespace
            return stripped_line[2:].strip()
        elif stripped_line == '#':
            # Handle case where there's only a hash with no content
            return ""
    
    # No h1 header found
    raise Exception("No h1 header found in markdown")
