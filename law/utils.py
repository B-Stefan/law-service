import os
from neo4j import GraphDatabase


def get_neo4j_driver_instance():
    return GraphDatabase.driver(os.getenv('NEO4J_URL', "bolt://localhost:7687"),
                        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "neo4jneo4j")))