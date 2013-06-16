from py2neo import neo4j, cypher

graph_db = neo4j.GraphDatabaseService()

def handle_row(row):
    print 'inside handle_row(row)'
    node = row[0]
    print node

def handle_repo(name,owner):
    print 'name: ' + name
    print 'owner: ' + owner

cypher.execute(graph_db, "START z=node(*) RETURN z", row_handler=handle_row)
