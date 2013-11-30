#!/usr/bin/env python

import github, time,sys

sys.path.append('./')
sys.path.append('../../../../')

from lib.logger import logger

from models.repository import Repository
from models.commit import Commit

from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker

class GitHubWorkerGetCommits(GitHubWorker):
    def starter(self):
        self.worker.set_client_id(Task.GET_COMMITS + '_' + str(self.threadID))
        self.worker.register_task(Task.GET_COMMITS, self.consume)

        print 'Starting GetCommits worker...'
        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        try:
            (owner, name) = gearman_job.data.split('/')

            ghRepository = self.gh.get_repo(gearman_job.data)
            dbRepository = Repository.get(owner, name)

            commits = ghRepository.get_commits()

            for commit in commits:
                print '%s - %s' % (self.threadID, commit.sha)

                print 'Try to add new commit - %s ...' % commit.sha
                dbCommit = Commit.add(commit, dbRepository[0])

                print 'Adding get commit comments task...'
                self.client.submit_job(Task.GET_COMMIT_COMMENTS, gearman_job.data+':'+str(commit.sha), background=True, max_retries=10)

                # todo: add fetching commit comments
        except github.UnknownObjectException as err:
            print "Repositorium %s/%s doesn't exist - omitting..." % (owner, name)
            logger.error("(%s) %s" % (__name__, str(err)))

            return 'ok'

        except github.GithubException as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            resetRateDate = self.gh.get_rate_limit().rate.reset
            self.show_time_rate_limit(resetRateDate)

            self.switch_token()

            #retry
            self.retry(Task.GET_COMMITS, gearman_job.data, future_date=resetRateDate)

            return 'error'
        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))

            return 'error'
        else:
            return 'ok'


if __name__ == "__main__":
    threads = []

    for num in xrange(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetCommits(num).start())

    #main loop
    while True:
        time.sleep(60)