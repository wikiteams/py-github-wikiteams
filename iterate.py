import sys, datetime, time
from py2neo import neo4j, cypher
from pygithub3 import Github, exceptions

PAGINATION_SIZE = 100
SLEEP_TIME = 5

my_config = {'verbose': sys.stderr}

graph_db = neo4j.GraphDatabaseService()

pass_string = open('pass.txt', 'r').read()
gh = Github(user='wikiteams',login='wikiteams',password=pass_string)
#gh.services.base.Service.set_user('wikiteams')
#repo_service = Repo(login='wikiteams',password='')

def json_s(n):
    return json_serialize(n)

def json_serialize(n):
    return str(n)

def handle_row(row):
    print 'inside handle_row(row)'
    node = row[0]
    print node
    #lista = str(node).split("/")
    #print lista
    #print 'len: ' + str(len(lista))
    #handle_repo(lista[3], lista[4].split("\"")[0])
    #print node['owner'] + " " + node['name']
    z = 0
    while True:
        try:
	    handle_repo(node,node['owner'],node['name'])
	    break
	except exceptions.NotFound:
	    print 'Ooops: error accessing data'
	    z += 1
	    if z>5:
	        break
	    time.sleep(SLEEP_TIME)
	except RuntimeError:
	    print 'Ooops: runtime error while accessing data'
	    z += 1
	    time.sleep(SLEEP_TIME)

def getdate():
    return datetime.datetime.now()

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
    node['watchers_pages_date'] = json_s(getdate())
    node['watchers'] = watchers_pages * PAGINATION_SIZE
    node['watchers_date'] = json_s(getdate())
    print 'saved watchers_pages'
    x = 1
    for page in watchers:
	print 'page no: ' + str(x)
	x += 1
	for resource in page:
	    print resource
	    rr = user_name(resource)
	    add_watcher(str(rr), name, owner)
    #watchers_count = len(watchers_list)
    #print coll.all()
    #result = repository.collaborators.list()
    #print result.all()
#    print owner
    for resource in coll.iterator():
	print resource
	rr = user_name(resource)
	add_collaborator(str(rr), name, owner)

def user_name(name):
    rr = str(name)
    rr = (rr.split("("))[1]
    rr = (rr.split(")"))[0]
    return str(rr)

def add_watcher(name,repo,owner):
    print 'check if doesnt exist'
    data = cypher.execute(graph_db, "START n=node(*) WHERE (n.type?=str('user') and n.name=str('" + name + "')) RETURN n")
    print 'before add watcher to DB'
    if len(data)<1:
	cypher.execute(graph_db, "CREATE (n {type: str('user'), name: str('" + name + "')})")
    print 'before cypher-ql add user as watcher'
    cypher.execute(graph_db, "START n=node(*), m=node(*) WHERE (n.type?=str('user') and n.name=str('" + name + "')) and (m.name=str('" + repo + "') and m.owner?=str('" + owner + "')) CREATE (n)-[r:WATCHES]->(m)")

def add_collaborator(name,repo,owner):
    print 'check if doesnt exist'
    data = cypher.execute(graph_db, "START n=node(*) WHERE (n.type?={user} and n.name={" + name + "}) RETURN n")
    print 'before add user to DB'
    if len(data)<1:
        cyper.execute(graph_db, "CREATE (n {type: {user}, name: {" + name + "}}")
    print 'before cypher-ql add user as collaborater'
    cyper.execute(graph_db, "START n=node(*), m=node(*) WHERE (n.type?={user} and n.name={" + name + "}) and (m.name={" + name + "} and m.owner?={" + owner + "}) CREATE (n)-[r:COLLABORATES]->(m)")
    print 'adding a collaborator ' + str(name) + ' to repo ' + str(repo)
    

cypher.execute(graph_db, "START z=node(*) WHERE id(z) > " + sys.argv[1] + " and id(z) < " + sys.argv[2] + " RETURN z", row_handler=handle_row)
