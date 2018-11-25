import os
from flask import Flask, jsonify
from neo4j import GraphDatabase

from law.service.law_service import LawService

app = Flask(__name__)

driver = GraphDatabase.driver(os.getenv('NEO4J_URL', "bolt://localhost:7687"),
                        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "neo4jneo4j")))
service = LawService()

@app.route('/api')
def api():

    data = service.get_law_paragraphs()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
