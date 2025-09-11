from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    """
    Enumeration of supported text formatting types in markdown.
    
    This enum defines the different types of text formatting that can be applied
    to text content when parsing markdown. Each type corresponds to a specific
    HTML tag or formatting style.
    """
    TEXT = "text"      # Plain text with no special formatting
    BOLD = "bold"      # Bold text (wrapped in <b> tags)
    ITALIC = "italic"  # Italic text (wrapped in <i> tags)
    CODE = "code"      # Inline code (wrapped in <code> tags)
    LINK = "link"      # Hyperlink (wrapped in <a> tags with href attribute)
    IMAGE = "image"    # Image (wrapped in <img> tags with src and alt attributes)


class TextNode:
    """
    Represents a piece of text with specific formatting type.
    
    TextNode is used to represent individual pieces of text content with their
    associated formatting type. It's the building block for parsing markdown
    text into structured format before converting to HTML.
    """
    
    def __init__(self, text, text_type, url=None):
        """
        Initialize a TextNode.
        
        Args:
            text (str): The actual text content.
            text_type (TextType): The type of formatting to apply to this text.
            url (str, optional): URL for links and images. Required for LINK and IMAGE types.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        """
        Check if two TextNode objects are equal.
        
        Two TextNodes are considered equal if they have the same text content,
        text type, and URL.
        
        Args:
            other: Another object to compare with.
            
        Returns:
            bool: True if the TextNodes are equal, False otherwise.
        """
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        """
        Return a string representation of the TextNode for debugging.
        
        Returns:
            str: String representation showing text content, type, and URL.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
