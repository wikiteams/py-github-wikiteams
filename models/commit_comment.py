import psycopg2, datetime
from lib.db import Database
from lib.exceptions import WikiTeamsNotFoundException
from lib.logger import logger

class CommitComment():
    @staticmethod
    def get(id):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.commits_comments WHERE id = %s ORDER BY fetched_at DESC LIMIT 1" % id
        cur.execute(sql)

        dbCommit = cur.fetchone()

        return dbCommit


    @staticmethod
    def add(repositoryId, comment):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            ghData = {
                'id': comment.id,
                'commit_id': comment.commit_id,
                'user_id': comment.user.id,
                'repository_id' : repositoryId,
                'body': comment.body,
                'path': comment.path,
                'line':  comment.line,
                'position': comment.position,
                'url': comment.url,
                'html_url': comment.html_url,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at,
                'fetched_at': datetime.datetime.utcnow()
            }

            sql = "INSERT INTO public.commits_comments (id, commit_id, user_id, repository_id, body, path, line, position, url, html_url, created_at, updated_at) " \
                  "VALUES (%(id)s, %(commit_id)s, %(user_id)s, %(repository_id)s, %(body)s, %(path)s, %(line)s, %(position)s, %(url)s, %(html_url)s, %(created_at)s, %(updated_at)s)"
            cur.execute(sql, ghData)

            return CommitComment.get(ghData['id'])
        except psycopg2.IntegrityError as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            if 'is not present in table' in str(err):
                if 'commit_id' in str(err):
                    logger.error("Raise WikiTeamsNotFoundException (Commit not found)")
                    raise WikiTeamsNotFoundException('Commit not found')
                elif 'user_id' in str(err):
                    logger.error("Raise WikiTeamsNotFoundException (User not found)")
                    raise WikiTeamsNotFoundException('User not found')
            else:
                print 'Commit comment exists!'

                return CommitComment.get(ghData['id'])

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
            raise