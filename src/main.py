from generate import copy_static_to_public, generate_pages_recursive

def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
