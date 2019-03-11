from law.api.law_resource import LawResource


class SearchAPI(LawResource):

    def get(self, search_term: str):
        return self.service.get_fulltext_result(search_term)