import psycopg2, threading, github

from gearman import GearmanWorker
from tools.queue.gearman import config

class GitHubWorker(threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        self.gh = github.Github(config.TOKEN)

        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        print 'Starting thread %s...' % self.threadID
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
        self.worker.register_task('contributors', self.consume)

        print 'Thread %s waiting for new tasks...' % self.threadID

        self.worker.work()


    def after_poll(self, any_activity):
        print 'Continue'
        return True


    def consume(self, gearman_worker, gearman_job):
        pass