import threading, github, datetime, json

from pytz import timezone
from gearman import GearmanWorker
from gearman.client import GearmanClient
from tools.queue.gearman import config
from lib.logger import logger

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
        self.client = GearmanClient(['localhost:4730'])


    def after_poll(self, any_activity):
        print 'Continue'
        return True

    def show_time_rate_limit(self, date):
        warsaw = timezone('Europe/Warsaw')
        rateDateTime = warsaw.localize(date)
        rateDateTime = rateDateTime + rateDateTime.utcoffset()
        print 'Rate limit to: %s' % rateDateTime

    def switch_token(self):
        tokens = len(config.TOKENS)

        if self.tokenIndex < tokens - 1:
            self.tokenIndex += 1
        else:
            self.tokenIndex = 0

        print "Switched to token: %s" % self.tokenIndex

        self.gh = github.Github(config.TOKENS[self.tokenIndex], per_page=100, timeout=90)

    def get_time_diff_in_seconds(self, future_date):
        return (future_date + datetime.timedelta(seconds=60) - datetime.datetime.utcnow()).seconds

    def retry(self, name, data, future_date=None, priority=None, increment_attempts=True):
        if future_date is not None:
            when_to_run = self.get_time_diff_in_seconds(future_date)
        else:
            when_to_run = None

        if when_to_run is None and priority is not None:
            background = True
        else:
            background = False

        if increment_attempts:
            data['attempts']  = int(data['attempts']) + 1

        if data['attempts'] < 10:
            if when_to_run is not None:
                print 'Retry current job in %s seconds' % when_to_run
            else:
                print 'Retry current job with priority %s' % priority

            self.client.submit_job(name, json.dumps(data), max_retries=10, when_to_run=when_to_run, priority=priority, background=background)
        else:
            print 'To many attempts... omitting job'
            logger.warning('To many attempts... omitting job')

    def starter(self):
        # todo: raise an exception
        pass


    def consume(self, gearman_worker, gearman_job):
        # todo: raise an exception
        pass