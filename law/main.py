from flask import Flask, jsonify

from law.service.law_service import LawService

app = Flask(__name__)
service = LawService()

@app.route('/api')
def api():

    data = service.get_law_paragraphs()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
