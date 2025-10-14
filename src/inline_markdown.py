import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)

        # Check for unclosed delimiter (odd number of parts means unclosed)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: unclosed delimiter '{delimiter}'")

        # Process the parts
        for i, part in enumerate(parts):
            if part == "":
                continue

            # Even indices are normal text, odd indices are delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    # Pattern: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # Pattern: [anchor text](url) but NOT ![alt](url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all images from the text
        images = extract_markdown_images(node.text)

        # If no images, keep the node as is
        if not images:
            new_nodes.append(node)
            continue

        # Process the text and split by images
        current_text = node.text
        for alt_text, url in images:
            # Split on the first occurrence of this image
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)

            if len(parts) == 2:
                # Add text before the image (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                # Add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                # Continue with the remaining text
                current_text = parts[1]

        # Add any remaining text after the last image
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all links from the text
        links = extract_markdown_links(node.text)

        # If no links, keep the node as is
        if not links:
            new_nodes.append(node)
            continue

        # Process the text and split by links
        current_text = node.text
        for anchor_text, url in links:
            # Split on the first occurrence of this link
            link_markdown = f"[{anchor_text}]({url})"
            parts = current_text.split(link_markdown, 1)

            if len(parts) == 2:
                # Add text before the link (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                # Add the link node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

                # Continue with the remaining text
                current_text = parts[1]

        # Add any remaining text after the last link
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply all splitting functions in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    # Split the markdown by double newlines
    blocks = markdown.split("\n\n")

    # Process each block: strip whitespace and filter out empty blocks
    result = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            result.append(stripped_block)

    return result
