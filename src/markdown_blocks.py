import re
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


def markdown_to_blocks(markdown):
    """Split markdown text into blocks separated by blank lines."""
    blocks = []
    raw_blocks = markdown.split('\n\n')

    for block in raw_blocks:
        # Strip whitespace from each block
        block = block.strip()
        # Only add non-empty blocks
        if block:
            blocks.append(block)

    return blocks


def block_to_block_type(block):
    """Determine the type of a markdown block."""
    # Check for heading (# to ######)
    if re.match(r'^#{1,6} ', block):
        return "heading"

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code"

    # Check for quote block (every line starts with >)
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return "quote"

    # Check for unordered list (every line starts with * or -)
    if all(line.startswith('* ') or line.startswith('- ') for line in lines):
        return "unordered_list"

    # Check for ordered list (every line starts with number. )
    if all(re.match(r'^\d+\. ', line) for line in lines):
        return "ordered_list"

    # Default to paragraph
    return "paragraph"


def split_nodes_image(old_nodes):
    """Split TextNodes on image markdown syntax."""
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in images:
            parts = text.split(f"![{alt}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """Split TextNodes on link markdown syntax."""
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text = node.text
        for anchor, url in links:
            parts = text.split(f"[{anchor}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """Convert text with inline markdown to a list of TextNodes."""
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_children(text):
    """Convert text with inline markdown to a list of HTMLNodes."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break

    # Extract text after the heading markers and space
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the ``` markers from start and end
    code_text = block[3:-3]
    # Strip only leading newline
    if code_text.startswith('\n'):
        code_text = code_text[1:]
    # Don't process inline markdown for code blocks
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split('\n')
    # Remove the > from each line
    quote_lines = [line[1:].strip() for line in lines]
    text = '\n'.join(quote_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split('\n')
    list_items = []

    for line in lines:
        # Remove the * or - and space
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split('\n')
    list_items = []

    for line in lines:
        # Remove the number and ". "
        text = re.sub(r'^\d+\. ', '', line)
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Replace single newlines with spaces for paragraph text
    text = block.replace('\n', ' ')
    children = text_to_children(text)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    """Convert a full markdown document to an HTMLNode."""
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            block_nodes.append(heading_to_html_node(block))
        elif block_type == "code":
            block_nodes.append(code_to_html_node(block))
        elif block_type == "quote":
            block_nodes.append(quote_to_html_node(block))
        elif block_type == "unordered_list":
            block_nodes.append(unordered_list_to_html_node(block))
        elif block_type == "ordered_list":
            block_nodes.append(ordered_list_to_html_node(block))
        else:  # paragraph
            block_nodes.append(paragraph_to_html_node(block))

    return ParentNode("div", block_nodes)
