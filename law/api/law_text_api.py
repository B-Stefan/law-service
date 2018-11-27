from law.api.law_resource import LawResource


class LawTextListAPI(LawResource):

    def get(self, paragraph_id:str):
        return self.service.get_text_paragraph_by_parent_id(paragraph_id)