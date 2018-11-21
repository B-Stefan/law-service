import unittest

from law.models.domain import Law, LawParagraph, TextParagraph


class DomainModelTest(unittest.TestCase):
    def test_law_create(self):

        id = "test"
        law = Law(id=id)

        self.assertEqual(law.id, id)

    def test_law_add_paragraph(self):
        number = "test"

        law = Law("My-Id")

        para = LawParagraph(number=number, name="Test")

        law.add_law_paragraph(para)

        expect = {
            number: para
        }

        self.assertDictEqual(law.children, expect)
        self.assertEqual(para.parent, law)

    def test_law_paragraph_create(self):
        number = "test"

        law = Law("test")

        para = LawParagraph(number=number, name="Test", parent=law)

        self.assertEqual(para.name, "Test")
        self.assertEqual(para.number, number)
        self.assertEqual(para.parent, law)
        self.assertEqual(para.id, "test-" + number)

    def test_law_paragraph_add_text_paragraphs(self):

        law = Law("test")

        para = LawParagraph(number="Test", name="Test", parent=law)

        number = "1"
        text = TextParagraph(text="My law text", number=number)

        para.add_text_paragraphs([text])

        self.assertEqual(len(para.children), 1)
        self.assertListEqual(para.children, [text])
        self.assertEqual(text.parent, para)

    def test_text_paragraph_create(self):
        number = "test"

        law = Law("test")

        para = LawParagraph(number=number, name="Test", parent=law)
        text = TextParagraph(number=number, text="my text", parent=para)

        self.assertEqual(text.text, "my text")
        self.assertEqual(text.number, number)
        self.assertEqual(text.parent, para)
        self.assertEqual(text.id, "test-test-" + number)