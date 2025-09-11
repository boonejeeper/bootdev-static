from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    Represents a parent node in the HTML tree structure.
    
    Parent nodes contain child HTMLNode objects and cannot have text content directly.
    They represent container elements in HTML that can hold other elements.
    Examples: <div>...</div>, <p>...</p>, <ul>...</ul>.
    """
    
    def __init__(self, tag: str, children: list, props: dict | None = None):
        """
        Initialize a ParentNode.
        
        Args:
            tag (str): The HTML tag name (e.g., 'div', 'p', 'ul'). Cannot be None or empty.
            children (list): List of child HTMLNode objects. Cannot be None or empty.
            props (dict | None): Dictionary of HTML attributes for the tag.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Convert the ParentNode to its HTML string representation.
        
        Recursively converts all child nodes to HTML and wraps them in the parent tag.
        
        Returns:
            str: The HTML string representation of this parent node and all its children.
                 Format: <tag props>child1_htmlchild2_html...</tag>
                 
        Raises:
            ValueError: If tag is None or empty, or if children list is None or empty.
            
        Examples:
            ParentNode("div", [LeafNode("p", "Hello")]) -> "<div><p>Hello</p></div>"
            ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")]) -> 
                "<ul><li>Item 1</li><li>Item 2</li></ul>"
        """
        # Validate required fields
        if self.tag is None or len(self.tag) == 0:
            raise ValueError("tags are required for ParentNodes")

        if self.children is None or len(self.children) == 0:
            raise ValueError("children are required for ParentNodes")

        # Build the props string if attributes are present
        props_string = ""
        if self.props is not None:
            props_string = " " + self.props_to_html()

        # Recursively convert all children to HTML
        child_elements = []
        for child in self.children:
            child_elements.append(child.to_html())

        # Build open and close tags
        open_tag_string = ""
        close_tag_string = ""
        if self.tag is not None:
            open_tag_string = f"<{self.tag}{props_string}>"
            close_tag_string = f"</{self.tag}>"

        # Combine everything: <tag>child1child2...</tag>
        return f"{open_tag_string}{''.join(child_elements)}{close_tag_string}"
