#!/usr/bin/env python

import psycopg2, sys, time, json

from gearman import GearmanClient

sys.path.append('./')
sys.path.append('../../../../')

from tools.queue.gearman.task import Task


class GitHubRepositoryClient():
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
        cur.execute("SELECT owner, name FROM public.repositories ORDER BY id")

        repositories = cur.fetchall()

        for repository in repositories:
            repositoryName = '%s/%s' % (repository[0], repository[1])

            data = {
                'repositoryName': repositoryName,
                'attempts': 0
            }

            print "\n\nAdding tasks for %s repository..." % repositoryName

            print 'Adding get contributors task...'
            self.client.submit_job(Task.GET_CONTRIBUTORS, json.dumps(data), background=True, max_retries=10)

            print 'Adding get languages task...'
            self.client.submit_job(Task.GET_LANGUAGES, json.dumps(data), background=True, max_retries=10)

            print 'Adding get repository readme task...'
            self.client.submit_job(Task.GET_REPOSITORY_README, json.dumps(data), background=True, max_retries=10)

            print 'Adding get issues task...'
            self.client.submit_job(Task.GET_ISSUES, json.dumps(data), background=True, max_retries=10)

            print 'Adding get commits task...'
            self.client.submit_job(Task.GET_COMMITS, json.dumps(data), background=True, max_retries=10)

            time.sleep(1)

if __name__ == "__main__":
    producer = GitHubRepositoryClient()
    producer.produce()