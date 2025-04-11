from shutil import copy, rmtree
from os import makedirs, mkdir, listdir
from os.path import dirname, isfile, join, abspath, exists
from converters import markdown_to_html_node

def copy_static_to_public(source=None, destination=None):
    if source is None:
        source = abspath("static")
        destination = abspath("docs")

    # delete everything in docs
        print("deleting docs/")
        rmtree("docs/", ignore_errors=True)
        print("creating docs/")
        mkdir("docs")

    # copy everything from static to docs
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
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found in text")


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    src_doc = ""    # This is the markdown text document
    template = ""   # This is the html template document

    with open(from_path) as file:
        src_doc = file.read()

    with open(template_path) as file:
        template = file.read()

    html_out = markdown_to_html_node(src_doc)
    title = extract_title(src_doc)

    out_doc = template.replace("{{ Title }}", title).replace("{{ Content }}", html_out.to_html())
    out_doc = out_doc.replace('href="/', f'href="{base_path}')
    out_doc = out_doc.replace('src="/', f'src="{base_path}')
        
    if not exists(dirname(dest_path)):
        print(f"'{dirname(dest_path)}' does not exist...creating path...")
        makedirs(dirname(dest_path))
    with open(dest_path, mode='w') as file:
        file.write(out_doc)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    print(f"dir_path:{dir_path_content}")
    dir_tree = listdir(dir_path_content)

    for item in dir_tree:
        if item == ".DS_Store":
            continue

        item_path = join(dir_path_content, item)

        if not isfile(item_path):
            template = abspath(template_path)
            new_dest = join(dest_dir_path, item)
            
            mkdir(new_dest)
            generate_pages_recursive(item_path, template, new_dest, base_path)

        if isfile(item_path):
            file_name = item.split(".")[0] + ".html"
            dest_path = join(dest_dir_path, file_name)
            
            generate_page(item_path, template_path, dest_path, base_path)

