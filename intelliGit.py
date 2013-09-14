from intelliRepository import MyRepository
from github import Github
import csv

repos = dict()
file_names = ['by-forks-20028-33', 'by-forks-20028-44',
              'by-watchers-3391-118', 'by-watchers-129-82',
              'by-watchers-82-70']


if __name__ == "__main__":
    '''
    Starts process of work on CSV files which are output of google bigquery
    whenever intelli_git.py is executed as an standalone program
    '''
    print 'start main'
    print 'Welcome to WikiTeams.pl GitHub repo getter!'

    pass_string = open('pass.txt', 'r').read()
    gh = Github('wikiteams', pass_string)

    for filename in file_names:
        print '------ WORKING WITH FILE : ' + filename
        with open('data\\' + filename + '.csv', 'rb') as source_csvfile:
            reposReader = csv.reader(source_csvfile,
                                     delimiter=',')
            reposReader.next()
            for row in reposReader:
                print 'row: ' + str(row)
                name = row[0]
                owner = row[1]

                #here eleminate repos without owner, rly

                forks = row[2]
                watchers = row[3]
                key = name + ',' + owner
                print 'key: ' + key
                repo = MyRepository()
                repo.setName(name)
                repo.setOwner(owner)
                repo.setWatchers(watchers)
                repo.setForks(forks)

                #check here if repo dont exist already in dictionary!

                repos[key] = repo
