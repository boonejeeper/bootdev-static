class HTMLNode:
    """
    Base class for representing HTML elements in a tree structure.
    
    This is an abstract base class that defines the common interface for all HTML nodes.
    It can represent both leaf nodes (with text content) and parent nodes (with child elements).
    """
    
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        """
        Initialize an HTMLNode.
        
        Args:
            tag (str | None): The HTML tag name (e.g., 'div', 'p', 'span'). None for text nodes.
            value (str | None): The text content for leaf nodes. None for parent nodes.
            children (list | None): List of child HTMLNode objects. None for leaf nodes.
            props (dict | None): Dictionary of HTML attributes (e.g., {'class': 'my-class', 'id': 'my-id'}).
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Convert the HTMLNode to its HTML string representation.
        
        This is an abstract method that must be implemented by subclasses.
        
        Returns:
            str: The HTML string representation of this node.
            
        Raises:
            NotImplementedError: Always raised since this is an abstract method.
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Convert the props dictionary to HTML attribute string.
        
        Returns:
            str: Space-separated string of HTML attributes in the format 'key="value"'.
                 Returns empty string if no props are defined.
                 
        Example:
            props = {'class': 'my-class', 'id': 'my-id'}
            Returns: 'class="my-class" id="my-id"'
        """
        if self.props is None:
            return ""

        prop_strings = []
        for key in self.props.keys():
            prop_strings.append(f'{key}="{self.props[key]}"')

        return " ".join(prop_strings)

    def __repr__(self):
        """
        Return a string representation of the HTMLNode for debugging.
        
        Returns:
            str: String representation showing all node properties.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        """
        Check if two HTMLNode objects are equal by comparing their string representations.
        
        Args:
            other: Another object to compare with.
            
        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        return self.__repr__() == other.__repr__()
