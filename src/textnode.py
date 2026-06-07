from enum import Enum

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
