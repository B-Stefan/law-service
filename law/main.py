
from flask import Flask, redirect
from flask_restful import Api

from law.api.law_api import LawListAPI
from law.api.law_paragraph_api import LawParagraphListAPI
from law.api.law_text_api import LawTextListAPI
from law.service.law_service import LawService
from law.utils import get_neo4j_driver_instance

app = Flask(__name__)

driver = get_neo4j_driver_instance()
service = LawService(driver)


def add_rest_api(law_service: LawService):
    api = Api(app, prefix="/api")
    api.add_resource(LawListAPI, '/law',  resource_class_kwargs={ 'law_service': law_service })
    api.add_resource(LawParagraphListAPI, '/law/<string:law_id>/paragraphs', resource_class_kwargs={ 'law_service': law_service})
    api.add_resource(LawTextListAPI, '/paragraph/<string:paragraph_id>/texts', resource_class_kwargs={ 'law_service': law_service})

swagger_url = "https://app.swaggerhub.com/apis-docs/B-Stefan/law-service/1.1.0"

@app.route('/')
def home():
    return redirect(swagger_url, code=302)

@app.route('/health')
def health():
    return "I'm healthy "

if __name__ == '__main__':
    add_rest_api(law_service=service)
    app.run()
