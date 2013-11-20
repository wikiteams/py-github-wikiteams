import github, time,sys

sys.path.append('../../../../')

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
            gh = github.Github(config.TOKEN)
            cur = self.db.cursor()

            repository = gh.get_repo(gearman_job.data)

            (owner, name) = gearman_job.data.split('/')

            sql = "SELECT * FROM public.repositories WHERE owner = '%s' AND name = '%s'" % (owner, name)
            cur.execute(sql)

            dbRepository = cur.fetchone()

            languages = repository.get_languages()

            for language in languages.keys():
                sql = "SELECT * FROM public.languages WHERE name = '%s'" % language

                cur.execute(sql)

                dbLanguage = cur.fetchone()

                if dbLanguage is None:
                    print 'Adding new language - %s ...' % language
                    sql = "INSERT INTO public.languages (id, name) VALUES (DEFAULT, '%s') RETURNING ID" % (language,)

                    cur.execute(sql)
                    self.db.commit()

                    id = cur.fetchone()[0]
                    dbLanguage = [id, language]

                sql = "SELECT * FROM public.repositories_languages WHERE repository_id = %s AND language_id = %s" % (dbRepository[0], dbLanguage[0])
                cur.execute(sql)

                repositoryLanguage = cur.fetchone()

                if repositoryLanguage is None:
                    print 'Linking language with repository...'
                    sql = "INSERT INTO public.repositories_languages (repository_id, language_id) VALUES (%s, %s)" % (dbRepository[0], dbLanguage[0])
                    cur.execute(sql)
                    self.db.commit()

                print '%s - %s' % (self.threadID, language)

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