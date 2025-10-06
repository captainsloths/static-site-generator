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
