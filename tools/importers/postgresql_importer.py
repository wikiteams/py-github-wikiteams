__author__ = 'snipe'

import csv, glob
import psycopg2

class PostgreSQLImporter():
    db = None
    csv_files = None
    csv_data = None
    first_row = None

    def __init__(self):
        self.get_csv_files()
        self.open_db()

    def get_csv_files(self):
        self.files = glob.glob('../../data/*.csv')
        return self.files

    def open_db(self):
        self.db = psycopg2.connect(database='wikiteams', user='wikiteams', password='wikiteams', host='localhost')

    def import_data(self):
        for file in self.files:
            self.first_row = None

            print file
            with open(file, 'rb') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')

                for row in reader:
                    if self.first_row is None:
                        self.first_row = row
                        continue

                    cur = self.db.cursor()

                    # add unique rows only
                    cur.execute("SELECT * FROM repositories WHERE name = %s AND owner = %s", (row[0], row[1]))
                    if cur.fetchone() is None:
                        cur.execute("INSERT INTO repositories (id, name, owner, forks, watchers) VALUES (DEFAULT, %s, %s, %s, %s)", row)
                        self.db.commit()

        self.db.close()

if __name__ == "__main__":
    importer = PostgreSQLImporter()
    importer.import_data()