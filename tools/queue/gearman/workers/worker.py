import threading, github

from pytz import timezone
from gearman import GearmanWorker
from gearman.client import GearmanClient
from tools.queue.gearman import config

class GitHubWorker(threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        self.tokenIndex = threadID

        # na kazdy watek osobny token
        self.gh = github.Github(config.TOKENS[self.tokenIndex])

        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        print 'Starting thread %s...' % self.threadID
        self.setup()
        self.starter()


    def setup(self):
        self.connect_gearman()


    def connect_gearman(self):
        self.worker = GearmanWorker(['localhost:4730'])


    def after_poll(self, any_activity):
        print 'Continue'
        return True

    def show_time_rate_limit(self):
        warsaw = timezone('Europe/Warsaw')
        rateDateTime = warsaw.localize(self.gh.get_rate_limit().rate.reset)
        rateDateTime = rateDateTime + rateDateTime.utcoffset()
        print 'Rate limit to: %s' % rateDateTime

    def switch_token(self):
        tokens = len(config.TOKENS)

        if self.tokenIndex < tokens - 1:
            self.tokenIndex += 1
        else:
            self.tokenIndex = 0

        print "Switched to token: %s" % self.tokenIndex

        self.gh = github.Github(config.TOKENS[self.tokenIndex])

    def retry(self, name, data):
        print 'Adding retry job...'
        client = GearmanClient(['localhost:4730'])
        client.submit_job(name, data, background=True, max_retries=10)
        del client

    def starter(self):
        # todo: raise an exception
        pass


    def consume(self, gearman_worker, gearman_job):
        # todo: raise an exception
        pass