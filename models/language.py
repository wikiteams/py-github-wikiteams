import psycopg2
from lib.db import Database

class Language():
    @staticmethod
    def add(language):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            sql = "INSERT INTO public.languages (id, name) VALUES (DEFAULT, '%s')" % (language,)
            cur.execute(sql)
        except psycopg2.IntegrityError as err:
            print 'Language exists!'

        except Exception as err:
            print 'Error: '
            print err
        finally:
            sql = "SELECT * FROM public.languages WHERE name = '%s'" % language
            cur.execute(sql)

            dbLanguage = cur.fetchone()

            return dbLanguage