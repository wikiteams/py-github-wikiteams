import github, time,sys

sys.path.append('../../../../')

from models.repository import Repository
from models.language import Language

from tools.queue.gearman import config
from tools.queue.gearman.task import Task
from tools.queue.gearman.workers.worker import GitHubWorker

class GitHubWorkerGetLanguages(GitHubWorker):
    def starter(self):
        self.worker.set_client_id(Task.GET_LANGUAGES + '_' + str(self.threadID))
        self.worker.register_task(Task.GET_LANGUAGES, self.consume)

        print 'Starting GetLanguages worker...'
        self.worker.work()

    def consume(self, gearman_worker, gearman_job):
        try:
            (owner, name) = gearman_job.data.split('/')

            ghRepository = self.gh.get_repo(gearman_job.data)
            dbRepository = Repository.get(owner, name)

            languages = ghRepository.get_languages()

            for language in languages.keys():
                print '%s - %s' % (self.threadID, language)

                print 'Try to add new language - %s ...' % language
                dbLanguage = Language.add(language)

                print 'Try to add link repository %s with language %s ...' % (gearman_job.data, language)
                bytes = languages[language]
                Repository.add_language(dbRepository[0], dbLanguage[0], bytes)

            return 'ok'
        except Exception as err:
            print err.message
            self.worker.send_job_failure(gearman_job)

            return 'error'

if __name__ == "__main__":
    threads = []

    for num in range(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetLanguages(num).start())

    #main loop
    while True:
        time.sleep(60)