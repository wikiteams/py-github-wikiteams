import psycopg2
from lib.db import Database
from lib.exceptions import WikiTeamsNotFoundException
from lib.logger import logger

class Language():
    @staticmethod
    def get(language):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        sql = "SELECT * FROM public.languages WHERE name = '%s' ORDER BY run_id DESC LIMIT 1" % language
        cur.execute(sql)

        dbLanguage = cur.fetchone()
        return dbLanguage

    @staticmethod
    def add(language, runId):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            sql = "INSERT INTO public.languages (id, name, run_id) VALUES (DEFAULT, '%s', %s)" % (language, runId)
            cur.execute(sql)

            return Language.get(language)

        except psycopg2.IntegrityError as err:
            logger.error("(%s) %s" % (__name__, str(err)))

            print 'Language exists!'

            return Language.get(language)

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
            raise