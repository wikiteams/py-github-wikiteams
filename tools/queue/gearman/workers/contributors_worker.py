import github, time,sys

sys.path.append('../../../../')

from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker


class GitHubWorkerGetContributors(GitHubWorker):
    def starter(self):
        self.worker.set_client_id('github_worker')
        self.worker.register_task(Task.GET_CONTRIBUTORS, self.consume)
        print 'Starting GetContributors worker...'

        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        gh = github.Github(config.TOKEN)

        repository = gh.get_repo(gearman_job.data)

        contributors = repository.get_contributors()

        for contributor in contributors:
            print '%s - %s' % (self.threadID, contributor.name)

        return 'ok'

if __name__ == "__main__":
    threads = []

    for num in range(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetContributors(num).start())

    #main loop
    while True:
        time.sleep(60)