import sys
from py2neo import neo4j, cypher
from pygithub3 import Github

my_config = {'verbose': sys.stderr}

graph_db = neo4j.GraphDatabaseService()

pass_string = open('pass.txt', 'r').read()
gh = Github(user='wikiteams',login='wikiteams',password=pass_string)
#gh.services.base.Service.set_user('wikiteams')
#repo_service = Repo(login='wikiteams',password='')

def handle_row(row):
    print 'inside handle_row(row)'
    node = row[0]
    print node
    #lista = str(node).split("/")
    #print lista
    #print 'len: ' + str(len(lista))
    #handle_repo(lista[3], lista[4].split("\"")[0])
    #print node['owner'] + " " + node['name']
    handle_repo(node,node['owner'],node['name'])

# function handle_repo
#
# node - entity of repository in our neo4j database
# owner - owner of repository
# name - name of repository
#
def handle_repo(node,owner,name):
    print 'name: ' + name
    print 'owner: ' + owner
    repository = gh.repos.get(user=owner,repo=name)
    print repository
    coll = gh.repos.collaborators.list(user=owner,repo=name)
    watchers = gh.repos.watchers.list(user=owner,repo=name)
    #watchers_list = list(watchers.get_page(1))
    watchers_pages = watchers.pages
    print 'Total pages: ' + str(watchers_pages)
    node['watchers_pages'] = watchers_pages
    print 'saved watchers_pages'
    #watchers_count = len(watchers_list)
    #print coll.all()
    #result = repository.collaborators.list()
    #print result.all()
    print owner
    for resource in coll.iterator():
	#add_collaborator(resource, repository, owner)
	print resource

def add_collaborator(name,repo,owner):
    cyper.execute(graph_db, "CREATE (n {type: user, name: {" + name + "}}")
    cyper.execute(graph_db, "START n=node(*), m=node(*) WHERE (n.type=user and n.name=" + name + ") and m.")
    print 'adding a collaborator ' + str(name) + ' to repo ' + str(repo)
    

cypher.execute(graph_db, "START z=node(*) WHERE id(z) > 0 and id(z) < " + sys.argv[1] + " RETURN z", row_handler=handle_row)
