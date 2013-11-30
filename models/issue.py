import psycopg2, base64
from lib.db import Database
from lib.exceptions import WikiTeamsNotFoundException
from lib.logger import logger

class Issue():
    @staticmethod
    def get(repositoryId, number):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.issues WHERE number = %s AND repository_id = %s ORDER BY fetched_at DESC LIMIT 1" % (number, repositoryId)
        cur.execute(sql)

        dbLanguage = cur.fetchone()
        return dbLanguage

    @staticmethod
    def add(repositoryId, issue):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        ghData = {
            'number': issue.number,
            'repository_id': repositoryId,
            'user_id': issue.user.id if issue.user is not None else None,
            'assignee_id': issue.assignee.id if issue.assignee is not None else None,
            'state': issue.state,
            'title': issue.title,
            'body': issue.body,
            'url': issue.url,
            'html_url': issue.html_url
        }

        try:
            sql = "INSERT INTO public.issues (number, repository_id, user_id, assignee_id, state, title, body, url, html_url) " \
                  "VALUES (%(number)s, %(repository_id)s, %(user_id)s, %(assignee_id)s, %(state)s, %(title)s, %(body)s, %(url)s, %(html_url)s)"
            cur.execute(sql, ghData)

            return Issue.get(repositoryId, issue.number)

        except psycopg2.IntegrityError as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            if 'is not present in table' in str(err):
                if 'user_id' in str(err):
                    logger.error("Raise WikiTeamsNotFoundException (Commit not found)")
                    raise WikiTeamsNotFoundException('User not found')
                elif 'assignee_id' in str(err):
                    logger.error("Raise WikiTeamsNotFoundException (Assignee not found)")
                    raise WikiTeamsNotFoundException('Assignee not found')
            else:
                print 'Issue exists!'

                return Issue.get(repositoryId, issue.number)

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
            raise