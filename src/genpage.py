import os
from markdowntotext import markdown_to_html_node, extract_title
def generate_page(from_path, template_path, dest_path, basepath):
    print(f" Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content1 = file.read()
        with open(template_path, "r") as temp_file:
            content2 = temp_file.read()
            html_nodes = markdown_to_html_node(content1)
            html = html_nodes.tohtml()
            title = extract_title(content1)
            page = content2.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", html)
            page = page.replace("href=\"/", f"href=\"{basepath}")
            page = page.replace("src=\"/", f"src=\"{basepath}")
            dest_dir = os.path.dirname(dest_path)
            os.makedirs(dest_dir, exist_ok=True)
            with open(dest_path, "w") as dest_file:
                dest_file.write(page)