import psycopg2
from lib.db import Database
from lib.logger import logger

class Repository():
    @staticmethod
    def get(repositoryOwner, repositoryName):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.repositories WHERE owner = '%s' AND name = '%s'" % (repositoryOwner, repositoryName)
        cur.execute(sql)

        dbRepository = cur.fetchone()

        return dbRepository


    @staticmethod
    def add_language(repositoryId, languageId, bytes):
        db = Database()
        cur = db.connection.cursor()

        try:
            sql = "INSERT INTO public.repositories_languages (repository_id, language_id, bytes) VALUES (%s, %s, %s)" % (repositoryId, languageId, bytes)
            cur.execute(sql)
        except psycopg2.IntegrityError as err:
            print 'Just linked!'
            logger.error("(%s) %s" % (__name__, str(err)))
        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))


    @staticmethod
    def add_contributor(repositoryId, userId):
        db = Database()
        cur = db.connection.cursor()

        try:
            sql = "INSERT INTO public.repositories_users (repository_id, user_id) VALUES (%s, %s)" % (repositoryId, userId)
            cur.execute(sql)
        except psycopg2.IntegrityError as err:
            print 'Just linked!'
            logger.error("(%s) %s" % (__name__, str(err)))
        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))