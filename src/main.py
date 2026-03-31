import os
import shutil
import sys
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    default_basepath = "/"
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    print("Public directory deleted.")
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)
    print("Content generated successfully.")
main()