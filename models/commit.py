import psycopg2
from lib.db import Database

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
                'author_id': commit.author.id,
                'committer_id': commit.committer.id,
                'message':  commit.commit.message,
                'additions': commit.stats.additions,
                'deletions': commit.stats.deletions
            }

            sql = "INSERT INTO public.commits (sha, repository_id, author_id, committer_id, message, additions, deletions) " \
                  "VALUES (%(sha)s, %(repository_id)s, %(author_id)s, %(committer_id)s, %(message)s, %(additions)s, %(deletions)s)"
            cur.execute(sql, ghData)
        except psycopg2.IntegrityError as err:
            print 'Commits exists!'

        except Exception as err:
            print 'Error: '
            print err
        finally:
            sql = "SELECT * FROM public.commits WHERE sha = %(sha)s AND repository_id = %(repository_id)s"
            cur.execute(sql, ghData)

            dbCommit = cur.fetchone()

            return dbCommit