#!/usr/bin/env python

import github, time,sys

sys.path.append('./')
sys.path.append('../../../../')

from lib.logger import logger

from models.repository import Repository
from models.commit_comment import CommitComment

from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker

class GitHubWorkerGetCommitComments(GitHubWorker):
    def starter(self):
        self.worker.set_client_id(Task.GET_COMMIT_COMMENTS + '_' + str(self.threadID))
        self.worker.register_task(Task.GET_COMMIT_COMMENTS, self.consume)

        print 'Starting GetCommitComments worker...'
        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        try:
            (repositoryName, commitSHA) = gearman_job.data.split(':')
            (owner, name) =  repositoryName.split('/')

            ghRepository = self.gh.get_repo(repositoryName)
            dbRepository = Repository.get(owner, name)

            commit = ghRepository.get_commit(commitSHA)
            comments = commit.get_comments()

            for comment in comments:
                print '%s - %s' % (self.threadID, str(commit.sha))

                print 'Try to add new commit comment - %s ...' % commit.sha
                dbCommitComment = CommitComment.add(dbRepository[0], comment)

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
        threads.append(GitHubWorkerGetCommitComments(num).start())

    #main loop
    while True:
        time.sleep(60)