import psycopg2, base64
from lib.db import Database
from lib.logger import logger

class Readme():
    @staticmethod
    def get(repositoryId):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.readmes WHERE repository_id = %s ORDER BY fetched_at DESC LIMIT 1" % repositoryId
        cur.execute(sql)

        dbLanguage = cur.fetchone()
        return dbLanguage

    @staticmethod
    def add(repositoryId, type, content):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        print 'base64'
        content = base64.b64decode(content)

        try:
            sql = "INSERT INTO public.readmes (repository_id, type, content) VALUES (%s, %s, %s)"
            cur.execute(sql, (repositoryId, type, content))

            return Readme.get(repositoryId)

        except psycopg2.IntegrityError as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            print 'Readme exists!'

            return Readme.get(repositoryId)

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
            raise