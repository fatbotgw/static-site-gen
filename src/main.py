import os
import sys
from generate import copy_static_to_public, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    content = os.path.join(os.getcwd(), 'content')
    template = os.path.join(os.getcwd(), 'template.html')
    docs  = os.path.join(os.getcwd(), 'docs')

    copy_static_to_public()
    generate_pages_recursive(content, template, docs, basepath)

if __name__ == "__main__":
    main()
