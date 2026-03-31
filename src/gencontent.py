import os
from pathlib import Path
from inline_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown content")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    directory = os.path.dirname(dest_path)
    if directory != "" :
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, filename)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, filename))
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(entry_path, template_path, dest_path)