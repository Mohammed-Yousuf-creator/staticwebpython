from textnode import TextNode, TextType,text_node_to_html_node
import re
from enum import Enum
from htmlnode import HTMLNode
from htmlnode import ParentNode
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_node != TextType.TEXT:
            new_list.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown: unmatched '{delimiter}' delimiter")
        for i, part in enumerate(parts):
            if len(part) == 0:
                continue
            if i % 2 == 0:
                new_list.append(TextNode(part, TextType.TEXT))
            else:
                new_list.append(TextNode(part, text_type))
    return new_list
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_node != TextType.TEXT:
            new_list.append(old_node) 
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0 or images is None:
            new_list.append(old_node)
            continue
        string = old_node.text
        for image in images:
            parts = string.split(f'![{image[0]}]({image[1]})', 1)
            if len(parts[0]) > 0:
                new_list.append(TextNode(parts[0], TextType.TEXT))
            new_list.append(TextNode(image[0], TextType.IMG, image[1]))
            string=parts[1]
        if len(string) > 0:
            new_list.append(TextNode(string, TextType.TEXT))
    return new_list
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_node != TextType.TEXT:
            new_list.append(old_node) 
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0 or links is None:
            new_list.append(old_node)
            continue
        string = old_node.text
        for link in links:
            parts = string.split(f'[{link[0]}]({link[1]})', 1)
            if len(parts[0]) > 0:
                new_list.append(TextNode(parts[0], TextType.TEXT))
            new_list.append(TextNode(link[0], TextType.LINK, link[1]))
            string = parts[1]
        if len(string) > 0:
            new_list.append(TextNode(string, TextType.TEXT))
    return new_list
def text_to_textnode(text):
    return split_nodes_link(
                split_nodes_image(
                    split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter(
                                [TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
                                ,"_", TextType.ITALIC)
                            ,"`",TextType.CODE)
                    )
            )
def markdown_to_blocks(markdown):
    lis = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block == "":
            continue
        lis.append(cleaned_block)
    return lis
class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QOUTE="qoute"
    UNORDERED_LIST="unordered list"
    ORDERED_LIST="ordered list"
def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QOUTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QOUTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith(("# ")):
            return line[2:].strip()
    raise Exception("No h1 header")