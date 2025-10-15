import os
import shutil
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node, extract_title


def copy_static_to_public(src_dir, dest_dir):
    """
    Recursively copies all contents from source directory to destination directory.
    Deletes destination directory first to ensure a clean copy.

    Args:
        src_dir: Source directory path
        dest_dir: Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting {dest_dir}...")
        shutil.rmtree(dest_dir)

    # Create the destination directory
    print(f"Creating {dest_dir}...")
    os.mkdir(dest_dir)

    # Recursively copy contents
    _copy_directory_contents(src_dir, dest_dir)


def _copy_directory_contents(src_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.

    Args:
        src_dir: Source directory path
        dest_dir: Destination directory path
    """
    # List all items in source directory
    items = os.listdir(src_dir)

    for item in items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # Create directory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(src_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.

    Args:
        from_path: Path to markdown file
        template_path: Path to HTML template file
        dest_path: Path to write the generated HTML file
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write the generated HTML
    with open(dest_path, 'w') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from all markdown files in a directory tree.

    Args:
        dir_path_content: Source directory containing markdown files
        template_path: Path to HTML template file
        dest_dir_path: Destination directory for generated HTML files
    """
    # List all items in the content directory
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            # If it's a markdown file, generate an HTML page
            if item.endswith('.md'):
                # Change .md extension to .html
                dest_path = dest_path.replace('.md', '.html')
                generate_page(src_path, template_path, dest_path)
        else:
            # If it's a directory, recursively process it
            generate_pages_recursive(src_path, template_path, dest_path)


def main():
    # Delete the public directory if it exists
    if os.path.exists("public"):
        print("Deleting public directory...")
        shutil.rmtree("public")

    # Copy static files to public directory
    copy_static_to_public("static", "public")

    # Generate all pages recursively from content directory
    generate_pages_recursive("content", "template.html", "public")

    print("\nSite generated successfully!")


if __name__ == "__main__":
    main()
