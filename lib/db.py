import psycopg2
from lib.singleton import singleton

@singleton
class Database:
    def __init__(self):
        self.connection = psycopg2.connect(database='wikiteams', user='wikiteams', password='wikiteams', host='localhost')