from typing import Dict, List

from law.models.domain import Law, TextParagraph, LawParagraph


class LawService():

    def __init__(self, driver):
        self.driver = driver

    def get_laws(self) -> List[str]:
        with self.driver.session() as session:
            return session.run('MATCH (x:LawParagraph) RETURN collect(distinct x.law)').single().value()

    def get_text_paragraph_by_parent_id(self, paragraph_id: str):
        with self.driver.session() as session:
            re = []
            for item in session.run('MATCH (t:TextParagraph)-[:HAS]-(p:LawParagraph) '
                                    'WHERE p.id={paragraph_id} '
                                    'RETURN t',
                                    {'paragraph_id': paragraph_id}):
                re.append(dict(item.value()))

            return re

    def get_law_paragraphs(self):
        with self.driver.session() as session:
            re = []
            for item in session.run('MATCH (a:LawParagraph) RETURN a'):
                re.append(dict(item.value()))

            return re

    def get_law_paragraphs_by_law(self, law_id: str):
        with self.driver.session() as session:
            re = []
            for item in session.run('MATCH (a:LawParagraph) '
                                    'WHERE a.law={law_id} '
                                    'RETURN a ', {'law_id': law_id}):
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

    def get_keywords_by_law_paragraph_id(self, id):
        with self.driver.session() as session:
            re = []
            for item in session.run('MATCH (a:LawParagraph {id: {id}})-[:MENTION]-(k:Keyword) '
                                    'RETURN k ', {'id': id}):
                re.append(dict(item.value()))

            return re

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
                ON CREATE SET p.text = ''
                SET p.text = p.text+{text_p_text}
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

    def merge_keywords(self, law_para: LawParagraph, keywords: List[str]):
        cypher = '''
                       MERGE (p:LawParagraph {id: {law_p_id}})
                       WITH p
                       UNWIND {keywords} as keyword
                       MERGE (k:Keyword {text: keyword})
                       MERGE (p)-[:MENTION]->(k)'''

        with self.driver.session() as session:
            session.run(cypher, {
                'law_p_id': law_para.id,
                'keywords': keywords,
            })