from enum import Enum


class TextType(Enum):
    PLAIN = "plain"         # normal text
    BOLD = "bold"           # bold text **asdf**
    ITALIC = "italic"       # italic text _asdf_
    CODE = "code"           # code `asdf` <- this is backtick
    LINK = "link"           # links [anchor text](url)
    IMAGE = "image"         # images ![alt text](url)


class TextNode:
    def __init__(self, text, text_type, url=None):
        if not text:
            raise ValueError("text must not be empty")
        self.text = text

        if not isinstance(text_type, TextType):
            raise ValueError("text_type must be an instance of TextType")
        self.text_type = text_type

        if text_type in {TextType.LINK, TextType.IMAGE} and not url:
            raise ValueError(f"url is required for text_type {text_type}")
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
