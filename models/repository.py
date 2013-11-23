import psycopg2
from lib.db import Database

class Repository():
    @staticmethod
    def get(repositoryOwner, repositoryName):
        db = Database()
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
            db.connection.commit()
        except psycopg2.IntegrityError as err:
            print 'Just linked!'
            db.connection.rollback()
