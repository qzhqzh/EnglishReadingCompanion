import configparser
import os
from py2neo import Node, Relationship

from core.models import Word, Article
from util import Neo4jOption




# class ArticleParser:
#     """ 文章解析器 """
#     title = str()
#     content = str()
#
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#
#
#     def save_words(words: iter):
#         wordss = []
#         for word in words:
#             w = Word()
#             w.spell = word
#         wordss.append(w)





if __name__ == '__main__':
    project_dir = os.getcwd()
    cfg = os.path.join(project_dir, 'config', 'config.ini')

    conf = configparser.ConfigParser()
    conf.read(cfg)

    uri = conf.get('neo4j', 'host')
    username = conf.get('neo4j', 'username')
    password = conf.get('neo4j', 'password')

    neo4j_option = Neo4jOption(uri, username, password)
    graph = neo4j_option.get_graph()

    # tx = graph.begin()
    # a = Node('Person', name='GGG')
    # b = Node('Person', name='TTT')
    # a['age'] = 20
    # b['age'] = 21
    # r = Relationship(a, 'KNOWS', b)
    # tx.create(a|b|r)
    # tx.commit()

    repo = neo4j_option.get_repository()

    alice = Article()
    alice.title = "A GOOD BOOK"

    repo.save(alice)

    repo.match(Article, "A GOOD BOOK").first()
    repo.match(Word, "book").first()
