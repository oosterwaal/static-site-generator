import os
import shutil


def copy_files_recursive(source_dir, dest_dir):
    # First, delete all contents of destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Get list of items in source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # It's a file, copy it
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # It's a directory, recursively copy it
            print(f"Copying directory: {source_path} -> {dest_path}")
            copy_files_recursive(source_path, dest_path)