import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        sections = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)", old_node.text)
        if len(sections) != len(images) + 1:
            raise ValueError("invalid markdown, image format error")
        for i in range(len(sections)):
            if sections[i] != "":
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(images):
                alt_text, url = images[i]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        sections = re.split(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", old_node.text)
        if len(sections) != len(links) + 1:
            raise ValueError("invalid markdown, link format error")
        for i in range(len(sections)):
            if sections[i] != "":
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(links):
                link_text, url = links[i]
                new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    return [line.strip() for line in lines if line.strip() != ""]
   
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST        
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            paragraph_children = text_to_children(block)
            paragraph_node = ParentNode("p", paragraph_children)
            children.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            level = len(parts[0])
            tag = f"h{level}"
            heading_children = text_to_children(parts[1])
            children.append(ParentNode(tag, heading_children))
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"
            code_text_node = TextNode(code_text, TextType.TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            code_leaf = ParentNode("code", [code_html_node])
            code_parent = ParentNode("pre", [code_leaf])
            children.append(code_parent)
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = []
            for line in lines:
                if line.startswith(">"):
                    cleaned.append(line[1:].lstrip())
            quote_text = "\n".join(cleaned)
            quote_children = text_to_children(quote_text)
            children.append(ParentNode("blockquote", quote_children))
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                if line.startswith("- "):
                    list_items.append(line[2:].lstrip())
            list_children = []
            for item in list_items:
                item_children = text_to_children(item)
                list_children.append(ParentNode("li", item_children))
            children.append(ParentNode("ul", list_children))
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                item_text = line.split(". ", 1)[1]
                list_items.append(item_text)
            list_children = []
            for item in list_items:
                item_children = text_to_children(item)
                list_children.append(ParentNode("li", item_children))
            children.append(ParentNode("ol", list_children))
    return ParentNode("div", children)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children
    