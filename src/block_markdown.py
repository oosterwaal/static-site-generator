import re
from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only include non-empty blocks
            filtered_blocks.append(stripped_block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    
    # Check for heading (1-6 # characters followed by space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with > followed by space or is just >)
    if all(line.startswith("> ") or line == ">" for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. )
    if len(lines) > 0:
        is_ordered_list = True
        for i, line in enumerate(lines):
            expected_number = i + 1
            if not line.startswith(f"{expected_number}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    return ParentNode("pre", [LeafNode("code", text)])


def olist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[3:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def ulist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def quote_to_html_node(block):
    lines = []
    for line in block.split("\n"):
        if line == ">":
            lines.append("")
        elif line.startswith("> "):
            lines.append(line[2:])  # Remove "> "
        else:
            raise ValueError("Invalid quote line")
    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = olist_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = ulist_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        else:
            raise ValueError(f"Unsupported block type: {block_type}")
        
        children.append(node)
    
    return ParentNode("div", children)