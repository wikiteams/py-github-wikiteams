#!/usr/bin/env python

import github, time, sys, json
from gearman.constants import PRIORITY_HIGH, PRIORITY_LOW

sys.path.append('./')
sys.path.append('../../../../')

from lib.logger import logger
from lib.exceptions import WikiTeamsNotFoundException

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
        data = json.loads(gearman_job.data)

        try:
            runId = data['runId']
            (owner, name) = data['repositoryName'].split('/')
            logger.info("Getting commits for repository %s" % data['repositoryName'])

            ghRepository = self.gh.get_repo(data['repositoryName'])
            dbRepository = Repository.get(owner, name)

            commits = ghRepository.get_commits()

            for commit in commits:
                print '%s - %s' % (self.threadID, commit.sha)

                print 'Try to add new commit - %s ...' % commit.sha
                dbCommit = Commit.add(commit, dbRepository[0], runId)

                if dbCommit is not None:
                    commitCommentData = {
                        'runId': runId,
                        'repositoryName': data['repositoryName'],
                        'commitSHA': commit.sha,
                        'attempts': 0
                    }

                    print 'Adding get commit comments task...'
                    self.client.submit_job(Task.GET_COMMIT_COMMENTS, json.dumps(commitCommentData), background=True, max_retries=10)

                print self.gh.rate_limiting

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
            self.retry(Task.GET_COMMITS, data, future_date=resetRateDate, increment_attempts=False)

            sleepTime = self.get_time_diff_in_seconds(resetRateDate)
            print 'Worker %s going to sleep for %s seconds [%s]' % (self.threadID, sleepTime, resetRateDate)
            time.sleep(sleepTime)

            return 'error'

        except WikiTeamsNotFoundException as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            contributorsData = {
                'runId': data['runId'],
                'repositoryName': data['repositoryName'],
                'attempts': 0
            }

            print 'Try to add contributors with high priority'
            self.client.submit_job(Task.GET_CONTRIBUTORS, json.dumps(contributorsData), background=True, max_retries=10, priority=PRIORITY_HIGH)

            # retry job
            self.retry(Task.GET_COMMITS, data, priority=PRIORITY_LOW)

            return 'error'

        except Exception as err:
            print 'Unknown error occurred'
            import traceback
            traceback.print_exc()
            logger.error("(%s) %s" % (__name__, str(err)))

            self.retry(Task.GET_COMMITS, data, priority=PRIORITY_LOW)

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