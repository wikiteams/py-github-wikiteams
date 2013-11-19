from gearman import GearmanWorker

import psycopg2, github, time, thread, threading

class GitHubConsumer(threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)


    def run(self):
        print 'Rozpoczynam %s' % self.threadID
        self.setup()
        self.starter()

    def setup(self):
        self.connect_gearman()
        self.open_db()

    def connect_gearman(self):
        self.worker = GearmanWorker(['localhost:4730'])

    def open_db(self):
        self.db = psycopg2.connect(database='wikiteams', user='wikiteams', password='wikiteams', host='localhost')

    def starter(self):
        self.worker.set_client_id('github_worker')
        self.worker.register_task('consume', self.consume)
        print 'startujemy'
        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        gh = github.Github(token)

        repository = gh.get_repo(gearman_job.data)

        contributors = repository.get_contributors()

        for contributor in contributors:
            print '%s - %s' % (self.threadID, contributor.name)

        return 'ok'

if __name__ == "__main__":
    threads = []

    for num in range(0, 10):
        threads.append(GitHubConsumer(num).start())