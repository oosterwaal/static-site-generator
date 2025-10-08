import os
import shutil
from textnode import TextNode, TextType
from copy_static import copy_files_recursive
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    """
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path) and item.endswith('.md'):
            # It's a markdown file, generate HTML
            relative_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))
            generate_page(item_path, template_path, dest_path)
            
        elif os.path.isdir(item_path):
            # It's a directory, recurse into it
            relative_dir = os.path.relpath(item_path, dir_path_content)
            dest_subdir = os.path.join(dest_dir_path, relative_dir)
            generate_pages_recursive(item_path, template_path, dest_subdir)


def main():
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    print("Starting static site generator...")
    
    # Delete anything in the public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)
    
    # Copy static files to public directory
    print(f"Copying files from {static_dir} to {public_dir}")
    copy_files_recursive(static_dir, public_dir)
    
    # Generate all pages recursively
    print(f"Generating pages from {content_dir} to {public_dir}")
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("Static site generation complete!")


if __name__ == "__main__":
    main()
