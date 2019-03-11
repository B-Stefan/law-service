from flask_restful import reqparse

from law.api.law_resource import LawResource


class SearchAPI(LawResource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str)

        args = parser.parse_args()

        return self.service.get_fulltext_result(args['q'])