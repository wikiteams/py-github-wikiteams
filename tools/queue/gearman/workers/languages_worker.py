#!/usr/bin/env python

import github, time, sys, json
from gearman.constants import PRIORITY_HIGH, PRIORITY_LOW

sys.path.append('./')
sys.path.append('../../../../')

from lib.logger import logger
from lib.exceptions import WikiTeamsNotFoundException

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
        data = json.loads(gearman_job.data)

        try:
            runId = data['runId']
            (owner, name) = data['repositoryName'].split('/')
            logger.info("Getting languages for repository %s" % data['repositoryName'])

            ghRepository = self.gh.get_repo(data['repositoryName'])
            dbRepository = Repository.get(owner, name)

            languages = ghRepository.get_languages()

            for language in languages.keys():
                print '%s - %s' % (self.threadID, language)

                print 'Try to add new language - %s ...' % language
                dbLanguage = Language.add(language, runId)

                print 'Try to add link repository %s with language %s ...' % (data['repositoryName'], language)

                bytes = languages[language]
                Repository.add_language(dbRepository[0], dbLanguage[0], runId, bytes)

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
            self.retry(Task.GET_LANGUAGES, data, future_date=resetRateDate, increment_attempts=False)

            return 'error'

        except WikiTeamsNotFoundException as err:
            logger.error("(%s) %s" % (__name__, str(err)))
            self.retry(Task.GET_LANGUAGES, data, priority=PRIORITY_LOW)

            return 'error'

        except Exception as err:
            print 'Unknown error occurred'
            import traceback
            traceback.print_exc()
            logger.error("(%s) %s" % (__name__, str(err)))

            self.retry(Task.GET_LANGUAGES, data, priority=PRIORITY_LOW)

            return 'error'
        else:
            return 'ok'


if __name__ == "__main__":
    threads = []

    for num in xrange(0, config.NUMBER_OF_THREADS):
        threads.append(GitHubWorkerGetLanguages(num).start())

    #main loop
    while True:
        time.sleep(60)