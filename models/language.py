import psycopg2
from lib.db import Database
from lib.logger import logger

class Language():
    @staticmethod
    def add(language):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            sql = "INSERT INTO public.languages (id, name) VALUES (DEFAULT, '%s')" % language
            cur.execute(sql)
        except psycopg2.IntegrityError as err:
            print 'Language exists!'
            logger.error("(%s) %s" % (__name__, str(err)))

        except Exception as err:
            print 'Unknown error occurred'
            logger.error("(%s) %s" % (__name__, str(err)))
        finally:
            sql = "SELECT * FROM public.languages WHERE name = %s ORDER BY fetched_at DESC LIMIT 1"
            cur.execute(sql, language)

            dbLanguage = cur.fetchone()

            return dbLanguage