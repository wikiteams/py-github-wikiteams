from py2neo import neo4j, cypher

graph_db = neo4j.GraphDatabaseService()

def handle_row(row):
    print 'inside handle_row(row)'
    node = row[0]
    print node
    lista = str(node).split("/")
    print lista
    print 'len: ' + str(len(lista))
    handle_repo(lista[3], lista[4].split("\"")[0])

def handle_repo(owner,name):
    print 'name: ' + name
    print 'owner: ' + owner

cypher.execute(graph_db, "START z=node(*) WHERE id(z) > 0  RETURN z", row_handler=handle_row)
