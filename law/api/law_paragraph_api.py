from law.api.law_resource import LawResource


class LawParagraphAPI(LawResource):

    def get(self, id):
        return self.service.get_law_paragraph_by_id(id)


class LawParagraphListAPI(LawResource):

    def get(self, law_id: str):
        return self.service.get_law_paragraphs_by_law(law_id)