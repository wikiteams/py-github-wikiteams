#!/usr/bin/env python

import github, time,sys

sys.path.append('./')
sys.path.append('../../../../')

from models.user import User
from models.repository import Repository
from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker


class GitHubWorkerGetContributors(GitHubWorker):
    def starter(self):
        self.worker.set_client_id(Task.GET_CONTRIBUTORS + '_' + str(self.threadID))
        self.worker.register_task(Task.GET_CONTRIBUTORS, self.consume)

        print 'Starting GetContributors worker...'
        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        try:
            (owner, name) = gearman_job.data.split('/')

            ghRepository = self.gh.get_repo(gearman_job.data)

            contributors = ghRepository.get_contributors()

            for ghContributor in contributors:
                print '%s - %s [%s]' % (self.threadID, ghContributor.login, ghContributor.name)

                print 'Try to add new user - %s ...' % ghContributor.login
                User.add_or_update(ghContributor)

                dbRepository = Repository.get(owner, name)

                print 'Try to add link repository %s with user %s ...' % (gearman_job.data, ghContributor.login)
                Repository.add_contributor(dbRepository[0], ghContributor.id)
        except github.GithubException as err:
            self.show_time_rate_limit()

            self.switch_token()

            #retry
            self.retry(Task.GET_CONTRIBUTORS, gearman_job.data)

            return 'error'
        else:
            return 'ok'

if __name__ == "__main__":
    threads = []

    for num in xrange(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetContributors(num).start())

    #main loop
    while True:
        time.sleep(60)