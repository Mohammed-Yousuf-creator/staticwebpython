from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT="plain"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMG="img"

class TextNode:
    def __init__(self, text, text_node, url=None):
        self.text = text
        self.text_node = text_node
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and self.text_node == other.text_node and self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_node.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_node:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        
        case TextType.IMG:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_node}")