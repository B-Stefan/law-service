import unittest

from law.models.domain import Law, LawParagraph, TextParagraph
from law.service.law_service import LawService
from law.utils import get_neo4j_driver_instance


def merge_text_paragraph(service: LawService,
                         law_id="law_test",
                         para_number="para_test",
                         text_number="text_test") -> TextParagraph:
    law = Law(law_id)
    para = LawParagraph(number=para_number, name="para_test_name", parent=law)
    text = TextParagraph(number=text_number,text="My text",  parent=para)
    service.merge_text_paragraph(text)
    return text

class LawServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = LawService(get_neo4j_driver_instance())

    def tearDown(self):
        self.service.purge_db()

    def test_law_service_create(self):

        service = LawService(get_neo4j_driver_instance())

        self.assertIsInstance(service, LawService)

    def test_merge_text_paragraph(self):

        law_id = "law_test"
        para_number = "para_test"
        merge_text_paragraph(self.service, law_id, para_number)

        id = law_id + "-" + para_number
        result = self.service.get_law_paragraph_by_id(id)

        self.assertIsNotNone(result)
        self.assertDictEqual(result,{
            'name': "para_test_name",
            'law': law_id,
            'number': para_number,
            'id': id
        })

    def test_get_paragraph_by_id(self):

        law_id = "law_test"
        para_number = "para_test"
        text = merge_text_paragraph(self.service, law_id, para_number)
        self.service.merge_text_paragraph(text)

        id = law_id + "-" + para_number
        result = self.service.get_law_paragraph_by_id(id)

        self.assertIsNotNone(result)
        self.assertDictEqual(result,{
            'name': "para_test_name",
            'law': law_id,
            'number': para_number,
            'id': id
        })

    def get_text_paragraph_by_parent_id(self):
        self.service.purge_db()
        merge_text_paragraph(self.service)
        merge_text_paragraph(self.service, para_number="444")
        merge_text_paragraph(self.service, law_id="bgb")
        texts = self.service.get_text_paragraph_by_parent_id("law_test-para_test")
        self.assertEqual(len(texts), 1)

    def test_get_laws(self):
        self.service.purge_db()
        merge_text_paragraph(self.service)
        merge_text_paragraph(self.service, law_id="bgb")
        laws = self.service.get_laws()
        print(laws)
        self.assertEqual(laws, ["law_test", "bgb"])

    def test_purge_db(self):
        merge_text_paragraph(self.service)
        self.service.purge_db()
        with self.service.driver.session() as session:
            count = session.run("MATCH (x) RETURN COUNT (x)").single().value()
            self.assertEqual(count, 0)