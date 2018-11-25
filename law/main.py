
from flask import Flask, jsonify
from law.service.law_service import LawService
from law.utils import get_neo4j_driver_instance

app = Flask(__name__)

driver = get_neo4j_driver_instance()
service = LawService(driver)

@app.route('/api')
def api():

    data = service.get_law_paragraphs()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
