from shutil import copy, rmtree
from os import makedirs, mkdir, listdir
from os.path import dirname, isfile, isdir, join, abspath, exists
from converters import markdown_to_html_node
from htmlnode import ParentNode

def copy_static_to_public(source=None, destination=None):
    if source is None:
        source = abspath("static")
        destination = abspath("public")

    # delete everything in public
        print("deleting public/")
        rmtree("public/", ignore_errors=True)
        print("creating public/")
        mkdir("public")

    # copy everything from static to public
    dir_tree = listdir(source)
    for item in dir_tree:
        if item == ".DS_Store":
            continue
        if not isfile(join(source, item)):
            mkdir(join(destination, item))
            copy_static_to_public(join(source, item), join(destination, item))

        if isfile(join(source, item)):
            copy(join(source, item), join(destination, item))

    return


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if markdown.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found in text")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    src_doc = ""    # This is the markdown text document
    template = ""   # This is the html template document

    with open(from_path) as file:
        src_doc = file.read()
        file.close()
    with open(template_path) as file:
        template = file.read()
        file.close()

    html_out = markdown_to_html_node(src_doc)
    title = extract_title(src_doc)

    out_doc = template.replace("{{ Title }}", title).replace("{{ Content }}", html_out.to_html())
        
    if not exists(dirname(dest_path)):
        print(f"'{dirname(dest_path)}' does not exist...creating path...")
        makedirs(dirname(dest_path))
    with open(dest_path, mode='w') as file:
        file.write(out_doc)
        file.close()
