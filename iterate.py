import sys
from py2neo import neo4j, cypher
from pygithub3 import Github

graph_db = neo4j.GraphDatabaseService()

gh = Github(user='wikiteams')
#repo_service = Repo(login='wikiteams',password='')

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
    repository = gh.repos.get(user=owner,repo=name)
    #print repository
    coll = gh.repos.collaborators.list(user=owner,repo=name)
    #print coll.all()
    #result = repository.collaborators.list()
    #print result.all()
    for resource in coll.iterator():
	add_collaborator(resource, repository)

def add_collaborator(name,repo):
    print 'adding a collaborator ' + str(name) + ' to repo ' + str(repo)
    

cypher.execute(graph_db, "START z=node(*) WHERE id(z) > 0 and id(z) < " + sys.argv[1] + " RETURN z", row_handler=handle_row)
