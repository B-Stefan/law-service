from typing import Dict, List


class TextParagraph:

    def __init__(self, number, text, parent = None):
        self.parent: LawParagraph = parent
        self.number: str = number
        self.text: str = text

    @property
    def id(self) -> str:
        safe_number = self.number if self.number is not None else ""
        return str.join("-", [self.parent.id, safe_number])


class LawParagraph:

    def __init__(self, name, number,  parent = None):
        self.parent: Law = parent
        self.name: str = name
        self.number = number
        self.children: List[TextParagraph] = []

    @property
    def id(self) -> str:
        return str.join("-", [self.parent.id, self.number])

    def add_text_paragraphs(self, array: List[TextParagraph]):
        for text in array:
            text.parent = self
        self.children = self.children + array


class Law:
    def __init__(self, id: str):
        self.id = id
        self.children: Dict[str, LawParagraph] = {}

    def add_law_paragraph(self, item: LawParagraph):
        self.children.update({item.number: item})
        item.parent = self


class Keyword:
    def __init__(self, text: str):
        self.text = text