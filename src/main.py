from textnode import TextNode,TextType
import os
import shutil
from genpage import generate_page
link = TextNode("this is some text",TextType.LINK,"https://boot.dev")
def copy(source, destination):

    source_directory = os.path.normpath(os.path.join("/home/mohammed_yousuf/workspace/bootdotdev/staticwebpython", source))
    target_directory = os.path.normpath(os.path.join("/home/mohammed_yousuf/workspace/bootdotdev/staticwebpython", destination))
    print(source_directory)
    print(target_directory)
    if os.path.isdir(target_directory):
        shutil.rmtree(target_directory)
    shutil.copytree(source_directory, target_directory)
def main():
    copy("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
if __name__ == "__main__":
    main()