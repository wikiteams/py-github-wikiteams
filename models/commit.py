import psycopg2, datetime
from lib.db import Database
from lib.logger import logger

class Commit():
    @staticmethod
    def add(commit, repositoryId):
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
                'fetched_at': datetime.datetime.utcnow()
            }

            sql = "INSERT INTO public.commits (sha, repository_id, author_id, committer_id, message, additions, deletions) " \
                  "VALUES (%(sha)s, %(repository_id)s, %(author_id)s, %(committer_id)s, %(message)s, %(additions)s, %(deletions)s)"
            cur.execute(sql, ghData)
        except psycopg2.IntegrityError as err:
            print 'Commits exists!'
            logger.error("(%s) %s" % (__name__, str(err)))

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
        finally:
            sql = "SELECT * FROM public.commits WHERE sha = %(sha)s AND repository_id = %(repository_id)s ORDER BY fetched_at DESC LIMIT 1"
            cur.execute(sql, ghData)

            dbCommit = cur.fetchone()

            return dbCommit