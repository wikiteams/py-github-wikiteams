import github, time,sys

sys.path.append('../../../../')

from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker

class GitHubWorkerGetCommits(GitHubWorker):
    def starter(self):
        self.worker.set_client_id('github_worker')
        self.worker.register_task(Task.GET_COMMITS, self.consume)
        print 'Starting GetContributors worker...'

        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        gh = github.Github(config.TOKEN)

        repository = gh.get_repo(gearman_job.data)

        contributors = repository.get_commits()

        for commit in commits:
            print '%s - %s' % (self.threadID, commit.name)

        return 'ok'

if __name__ == "__main__":
    threads = []

    for num in range(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetCommits(num).start())

    #main loop
    while True:
        time.sleep(60)