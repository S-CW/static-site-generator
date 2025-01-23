import code
from enum import Enum
from unittest.util import unorderable_list_difference

from hamcrest import starts_with

from htmlnode import ParentNode
from util import text_node_to_html, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks    
    
    
def block_to_block_type(block):
    lines = block.split("\n")
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "##### ")):
        return BlockType.HEADING.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not line.startswith("* ") and not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.ULIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.OLIST.value
    return BlockType.PARAGRAPH.value


def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case "paragraph":
            return paragraph_to_html_node(block)
        case "heading":
            return heading_to_html_node(block)
        case "code":
            return code_to_html_node(block)
        case "quote":
            return quote_to_html_node(block)
        case "unordered_list":
            return ulist_to_html_node(block)
        case "ordered_list":
            return olist_to_html_node(block)

# handle inline markdown and convert to html node
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        html_children.append(html_node)
    return html_children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    html_children = text_to_children(paragraph)
    return ParentNode("p", html_children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#": level += 1
        else: break
    if level + 1 >= len(block):
        raise ValueError("Invalid heading")
    content = block[level:].strip()
    html_children = text_to_children(content)
    return ParentNode(f"h{level}", html_children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    content = block[3: -3].strip()
    html_children = text_to_children(content)
    code = ParentNode("code", html_children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    lines = block.splitlines()
    html_nodes = []
    for line in lines:
        content = line.lstrip("1234567890. ")
        child_nodes = text_to_children(content)
        html_nodes.append(ParentNode("li", child_nodes))
    return ParentNode("ol", html_nodes)


def ulist_to_html_node(block):
    lines = block.splitlines()
    html_nodes = []
    for line in lines:
        content = line[2:]
        child_nodes = text_to_children(content)
        html_nodes.append(ParentNode("li", child_nodes))
    return ParentNode("ul", html_nodes)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip("> "))
    content = " ".join(new_lines)
    html_children = text_to_children(content)
    
    return ParentNode("blockquote", html_children)