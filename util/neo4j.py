from py2neo import Graph
from py2neo.ogm import Repository


class Neo4jOption:
    """ Neo4j 客户端 """
    uri = str()
    username = str()
    password = str()
    client = None

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def get_graph(self):
        self.http_port = 7474
        self.uri = f"http://{self.host}:{self.http_port}"
        return Graph(self.uri, username=self.username, password=self.password)

    def get_repository(self):
        self.bolt_port = 7687
        self.uri = f"bolt://{self.username}@{self.host}:{self.bolt_port}"
        return Repository(self.uri, password=self.password)
