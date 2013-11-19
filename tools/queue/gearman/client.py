from gearman import GearmanClient

import psycopg2, github, time

class GitHubProducer():
    db = None
    csv_files = None
    csv_data = None
    first_row = None

    def __init__(self):
        self.connect_gearman()
        self.open_db()

    def connect_gearman(self):
        self.client = GearmanClient(['localhost:4730'])

    def open_db(self):
        self.db = psycopg2.connect(database='wikiteams', user='wikiteams', password='wikiteams', host='localhost')

    def produce(self):
        cur = self.db.cursor()
        cur.execute("SELECT owner, name FROM public.repositories LIMIT 100")

        repositories = cur.fetchall()

        for repository in repositories:
            repositoryName = '%s/%s' % (repository[0], repository[1])
            print repositoryName
            self.client.submit_job('consume', repositoryName, background=True)

if __name__ == "__main__":
    producer = GitHubProducer()
    producer.produce()