from os import close
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    Represents a leaf node in the HTML tree structure.
    
    Leaf nodes contain text content and cannot have children. They represent
    the terminal elements in an HTML tree, such as text nodes or self-closing tags.
    Examples: <b>bold text</b>, <i>italic text</i>, plain text content.
    """
    
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        """
        Initialize a LeafNode.
        
        Args:
            tag (str | None): The HTML tag name (e.g., 'b', 'i', 'code'). 
                             None for plain text nodes.
            value (str): The text content of the node. Cannot be None.
            props (dict | None): Dictionary of HTML attributes for the tag.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Convert the LeafNode to its HTML string representation.
        
        Returns:
            str: The HTML string representation of this leaf node.
                 Format: <tag props>value</tag> or just 'value' for text nodes.
                 
        Raises:
            ValueError: If the node's value is None.
            
        Examples:
            LeafNode("b", "bold text") -> "<b>bold text</b>"
            LeafNode(None, "plain text") -> "plain text"
            LeafNode("a", "link", {"href": "http://example.com"}) -> '<a href="http://example.com">link</a>'
        """
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")

        # Build the props string if attributes are present
        props_string = ""
        if self.props is not None:
            props_string = " " + self.props_to_html()

        # Build open and close tags
        open_tag_string = ""
        close_tag_string = ""
        if self.tag is not None:
            open_tag_string = f"<{self.tag}{props_string}>"
            close_tag_string = f"</{self.tag}>"

        return f"{open_tag_string}{self.value}{close_tag_string}"
