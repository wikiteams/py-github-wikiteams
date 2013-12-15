import psycopg2, datetime
from lib.db import Database
from lib.exceptions import WikiTeamsNotFoundException
from lib.logger import logger

class Commit():
    @staticmethod
    def get(sha, repository_id):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.commits WHERE sha = %s AND repository_id = %s ORDER BY run_id DESC LIMIT 1"
        cur.execute(sql, (sha, repository_id))

        dbCommit = cur.fetchone()
        return dbCommit


    @staticmethod
    def add(commit, repositoryId, runId):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            ghData = {
                'sha': commit.sha,
                'repository_id': repositoryId,
                'author_id': commit.author.id if commit.author is not None else None,
                'committer_id': commit.committer.id if commit.committer is not None else None,
                'message':  commit.commit.message,
                'additions': commit.stats.additions,
                'deletions': commit.stats.deletions,
                'fetched_at': datetime.datetime.utcnow(),
                'run_id': runId
            }

            sql = "INSERT INTO public.commits (sha, repository_id, author_id, committer_id, message, additions, deletions, run_id) " \
                  "VALUES (%(sha)s, %(repository_id)s, %(author_id)s, %(committer_id)s, %(message)s, %(additions)s, %(deletions)s, %(run_id)s)"
            cur.execute(sql, ghData)

            return Commit.get(ghData['sha'], ghData['repository_id'])

        except psycopg2.IntegrityError as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            if 'is not present in table' in str(err):
                print 'Object does not exist'

                if 'author_id' in str(err):
                    raise WikiTeamsNotFoundException('Author not found')
                elif 'committer_id' in str(err):
                    raise WikiTeamsNotFoundException('Committer not found')
            else:
                print 'Commits exists!'

                return None #Commit.get(ghData['sha'], ghData['repository_id'])

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
            raise