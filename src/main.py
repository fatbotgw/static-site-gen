from textnode import TextType
from textnode import TextNode


def main():
    text = "This is some text"
    text_type = TextType.LINK
    url = "https://www.boot.dev"
    test_node = TextNode(text, text_type, url)
    print(test_node)


if __name__ == "__main__":
    main()
