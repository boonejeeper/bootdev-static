"""
Main module for the static site generator.

This module provides the main entry point for the static site generator.
It handles copying static assets from the source directory to the public
directory where the generated site will be served from.
"""

import os
import sys
import shutil
from textnode import TextNode, TextType
from nodeutilities import markdown_to_html_node, extract_title


def copy_static_to_public(source_dir, dest_dir):
    """
    Recursively copies all contents from source_dir to dest_dir.
    
    This function ensures a clean copy by first deleting the destination
    directory if it exists, then recursively copying all files and subdirectories
    from the source to the destination.
    
    Args:
        source_dir (str): The source directory to copy from (e.g., "static").
        dest_dir (str): The destination directory to copy to (e.g., "public").
        
    Example:
        copy_static_to_public("static", "public")
        # Copies all files from static/ to public/
    """
    print(f"Starting copy from {source_dir} to {dest_dir}")
    
    # Delete destination directory if it exists to ensure clean copy
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Created directory: {dest_dir}")
    
    # Copy all contents recursively
    _copy_recursive(source_dir, dest_dir)
    print("Copy completed successfully!")


def _copy_recursive(source_path, dest_path):
    """
    Helper function to recursively copy files and directories.
    
    This is a private helper function that handles the actual recursive
    copying logic. It processes both files and directories, creating
    the appropriate destination structure.
    
    Args:
        source_path (str): The source file or directory path.
        dest_path (str): The destination file or directory path.
    """
    if not os.path.exists(source_path):
        print(f"Warning: Source path does not exist: {source_path}")
        return
    
    if os.path.isfile(source_path):
        # Copy file using shutil.copy2 to preserve metadata
        shutil.copy2(source_path, dest_path)
        print(f"Copied file: {source_path} -> {dest_path}")
    elif os.path.isdir(source_path):
        # Create destination directory
        os.makedirs(dest_path, exist_ok=True)
        print(f"Created directory: {dest_path}")
        
        # Recursively copy all contents of the directory
        for item in os.listdir(source_path):
            source_item = os.path.join(source_path, item)
            dest_item = os.path.join(dest_path, item)
            _copy_recursive(source_item, dest_item)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    
    This function reads a markdown file, converts it to HTML using the markdown
    parser, extracts the title, and replaces placeholders in a template file
    to create the final HTML page.
    
    Args:
        from_path (str): Path to the source markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path where the generated HTML file should be saved.
        basepath (str): The base path for the site. Defaults to "/".
        
    Example:
        generate_page("content/index.md", "template.html", "public/index.html", "/my-site")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title from markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    html_page = template_content.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
    
    # Replace href="/ and src="/ patterns with basepath
    if basepath != "/":
        html_page = html_page.replace('href="/', f'href="{basepath}/')
        html_page = html_page.replace('src="/', f'src="{basepath}/')
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML page
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html_page)


def find_markdown_files(content_dir):
    """
    Recursively find all markdown files in the content directory.
    
    Args:
        content_dir (str): Path to the content directory.
        
    Returns:
        list: List of paths to markdown files relative to content_dir.
    """
    markdown_files = []
    
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                # Get relative path from content_dir
                rel_path = os.path.relpath(os.path.join(root, file), content_dir)
                markdown_files.append(rel_path)
    
    return markdown_files


def get_html_path(markdown_path):
    """
    Convert a markdown file path to an HTML file path.
    
    Args:
        markdown_path (str): Path to markdown file relative to content directory.
        
    Returns:
        str: Corresponding HTML path relative to public directory.
    """
    # Replace .md extension with .html
    html_path = markdown_path.replace('.md', '.html')
    return html_path


def generate_pages_recursively(content_dir, template_path, public_dir, basepath="/"):
    """
    Recursively generate HTML pages from all markdown files in content directory.
    
    Args:
        content_dir (str): Path to the content directory.
        template_path (str): Path to the HTML template file.
        public_dir (str): Path to the public directory where HTML files will be generated.
        basepath (str): The base path for the site. Defaults to "/".
    """
    print(f"Finding markdown files in {content_dir}")
    markdown_files = find_markdown_files(content_dir)
    
    print(f"Found {len(markdown_files)} markdown files:")
    for file in markdown_files:
        print(f"  - {file}")
    
    for markdown_file in markdown_files:
        # Get full paths
        source_path = os.path.join(content_dir, markdown_file)
        html_file = get_html_path(markdown_file)
        dest_path = os.path.join(public_dir, html_file)
        
        # Generate the HTML page
        generate_page(source_path, template_path, dest_path, basepath)


def main():
    """
    Main entry point for the static site generator.
    
    This function orchestrates the static site generation process.
    It deletes the docs directory, copies static assets, and generates
    all HTML pages from markdown content recursively.
    
    Command line usage:
        python main.py [basepath]
    
    Args:
        basepath (str, optional): The base path for the site. Defaults to "/".
    """
    # Get basepath from command line arguments, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        # Ensure basepath starts with "/" and doesn't end with "/" (except for root)
        if not basepath.startswith("/"):
            basepath = "/" + basepath
        if basepath != "/" and basepath.endswith("/"):
            basepath = basepath.rstrip("/")
    
    print(f"Using basepath: {basepath}")
    
    # Delete anything in the docs directory
    if os.path.exists("docs"):
        print("Removing existing docs directory")
        shutil.rmtree("docs")
    
    # Copy all static files from static to docs
    copy_static_to_public("static", "docs")
    
    # Generate all HTML pages from markdown files recursively
    generate_pages_recursively("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
