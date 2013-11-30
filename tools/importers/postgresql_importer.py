#!/usr/bin/env python

import csv, glob, psycopg2, datetime

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


                    dataMapper = {
                        'owner': row[1],
                        'name': row[0],
                        'full_name': '',
                        'description': '',
                        'private': False,
                        'fork': False,
                        'url': '',
                        'html_url': '',
                        'clone_url': '',
                        'git_url': '',
                        'ssh_url': '',
                        'svn_url': '',
                        'mirror_url': '',
                        'homepage': '',
                        'forks_count': row[2],
                        'stargazers_count': 0,
                        'watchers_count': row[3],
                        'size': 0,
                        'master_branch': 'master',
                        'open_issues_count': 0,
                        'pushed_at': datetime.datetime.utcnow(),
                        'created_at': datetime.datetime.utcnow(),
                        'subscribers_count': 0,
                        'has_issues': True,
                        'has_wiki': True,
                        'has_downloads': True,
                    }

                    cur = self.db.cursor()

                    # add unique rows only
                    cur.execute("SELECT * FROM repositories WHERE name = %(name)s AND owner = %(owner)s", dataMapper)
                    if cur.fetchone() is None:
                        cur.execute("INSERT INTO repositories (id, owner, name, full_name, description, private, fork, url, "
                                    "html_url, clone_url, git_url, ssh_url, svn_url, mirror_url, homepage, forks_count, "
                                    "stargazers_count, watchers_count, size, master_branch, open_issues_count, pushed_at, "
                                    "created_at, subscribers_count, has_issues, has_wiki, has_downloads) "
                                    "VALUES (DEFAULT, %(owner)s, %(name)s, %(full_name)s, %(description)s, %(private)s, "
                                    "%(fork)s, %(url)s, %(html_url)s, %(clone_url)s, %(git_url)s, %(ssh_url)s, %(svn_url)s, "
                                    "%(mirror_url)s, %(homepage)s, %(forks_count)s, %(stargazers_count)s, %(watchers_count)s, "
                                    "%(size)s, %(master_branch)s, %(open_issues_count)s, %(pushed_at)s, %(created_at)s, "
                                    "%(subscribers_count)s, %(has_issues)s, %(has_wiki)s, %(has_downloads)s)", dataMapper)
                        self.db.commit()

        self.db.close()

if __name__ == "__main__":
    importer = PostgreSQLImporter()
    importer.import_data()