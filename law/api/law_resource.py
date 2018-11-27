from flask_restful import Resource
from law.service.law_service import LawService

class LawResource(Resource):

    def __init__(self, **kwargs):
        # law_service is a black box dependency
        self.service: LawService = kwargs['law_service']