import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(source_dir_path):
        source_item_path = os.path.join(source_dir_path, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        print(f" * {source_item_path} -> {dest_item_path}")
        
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, dest_item_path)
        else:
            copy_files_recursive(source_item_path, dest_item_path)

    
    