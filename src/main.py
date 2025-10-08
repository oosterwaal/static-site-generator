import os
import shutil
import sys
from textnode import TextNode, TextType
from copy_static import copy_files_recursive
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    """
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path) and item.endswith('.md'):
            # It's a markdown file, generate HTML
            relative_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))
            generate_page(item_path, template_path, dest_path, basepath)
            
        elif os.path.isdir(item_path):
            # It's a directory, recurse into it
            relative_dir = os.path.relpath(item_path, dir_path_content)
            dest_subdir = os.path.join(dest_dir_path, relative_dir)
            generate_pages_recursive(item_path, template_path, dest_subdir, basepath)


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths - now using docs instead of public
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    print("Starting static site generator...")
    print(f"Using basepath: {basepath}")
    
    # Delete anything in the docs directory
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    os.makedirs(docs_dir)
    
    # Copy static files to docs directory
    print(f"Copying files from {static_dir} to {docs_dir}")
    copy_files_recursive(static_dir, docs_dir)
    
    # Generate all pages recursively
    print(f"Generating pages from {content_dir} to {docs_dir}")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    
    print("Static site generation complete!")


if __name__ == "__main__":
    main()
