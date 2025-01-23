from genericpath import isdir, isfile
import os
import shutil
from textnode import TextNode, TextType

def main():
    print("Copying static files to public directory...")
    copy_files_recursive("static", "public")


def copy_files_recursive(source_dir, dest_dir):
    # delete folder and its files
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    
    list_dir = os.listdir(source_dir)
    for item in list_dir:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f" * {source_path} -> {dest_path}")
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        if os.path.isdir(source_path):
            copy_files_recursive(source_path, dest_path)
    
    
if __name__ == "__main__":
    main()