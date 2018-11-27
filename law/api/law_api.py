from law.api.law_resource import LawResource


class LawListAPI(LawResource):

    def get(self):
        return self.service.get_laws()