from typing import Dict

from law.models.domain import Law, TextParagraph


class LawService():

    def __init__(self, driver):
        self.driver = driver

    def get_law_paragraphs(self):
        with self.driver.session() as session:
            re = []
            for item in session.run('MATCH (a:LawParagraph) RETURN a'):
                re.append(dict(item.value()))

            return re

    def get_law_paragraph_by_id(self, id):
        with self.driver.session() as session:
            result = session.run('''
                    MATCH (a:LawParagraph)
                    WHERE a.id = {id}
                    RETURN a
            ''', id=id).single().value()

            return dict(result)

    def merge_laws(self, laws: Dict[str, Law]):

        for key, law in laws.items():
            for key, law_para in law.children.items():
                for text_para in law_para.children:
                    self.merge_text_paragraph(text_para)

    def purge_db(self):
        with self.driver.session() as session:
            session.run("MATCH (x) DETACH DELETE x")

    def merge_text_paragraph(self, item: TextParagraph):
        cypher = '''
                MERGE (p:TextParagraph {id: {text_p_id}})
                SET p.text = {text_p_text}
                SET p.number = {text_p_mumber}
                MERGE (l:LawParagraph {id: {law_p_id}})
                SET l.name = {law_p_name}
                SET l.number = {law_p_number}
                SET l.law = {law_id}
                MERGE (p)-[:HAS]-(l)'''

        with self.driver.session() as session:
            session.run(cypher, {
                'text_p_id': item.id,
                'text_p_text': item.text,
                'text_p_mumber': item.number,
                'law_p_id': item.parent.id,
                'law_p_name': item.parent.name,
                'law_p_number': item.parent.number,
                'law_id': item.parent.parent.id
            })
