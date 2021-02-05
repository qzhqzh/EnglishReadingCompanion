

from py2neo import Graph, Node, Relationship
test_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="zhuqin"
)
a = Node('Person', name='Alice')
b = Node('Person', name='Bob')
test_graph.create(a)
test_graph.create(b)
r = Relationship(a, 'KNOWS', b)
test_graph.create(r)
print(a, b, r)
a['age'] = 20
b['age'] = 21
r['time'] = '2017/08/31'
print(a, b, r)