'''
WikiTeams.pl top 32000 repos dataset creator
Please keep this file with PEP8 standard
Dont fork without good reason, use clone instead

@since 1.1
@author Oskar Jarczyk
'''

from intelliRepository import MyRepository
from github import Github, Repository, GithubException
import csv
import scream

repos = dict()
file_names = ['by-forks-20028-33', 'by-forks-20028-44',
              'by-watchers-3391-118', 'by-watchers-129-82',
              'by-watchers-82-70']


if __name__ == "__main__":
    '''
    Starts process of work on CSV files which are output of google bigquery
    whenever intelli_git.py is executed as an standalone program
    '''
    scream.say('start main')
    scream.say('Welcome to WikiTeams.pl GitHub repo getter!')

    pass_string = open('pass.txt', 'r').read()
    gh = Github('wikiteams', pass_string)

    for filename in file_names:
        scream.say('------ WORKING WITH FILE : ' + filename)
        with open('data\\' + filename + '.csv', 'rb') as source_csvfile:
            reposReader = csv.reader(source_csvfile,
                                     delimiter=',')
            reposReader.next()
            for row in reposReader:
                scream.log('Processing row: ' + str(row))
                name = row[0]
                owner = row[1]

                #here eleminate repos without owner, rly
                if len(owner.strip()) < 1:
                    scream.log('Skipping orphan repo: ' + name)
                    continue
                    #print 'length < 1'

                forks = row[2]
                watchers = row[3]
                key = owner + '/' + name
                scream.log('Key built: ' + key)

                repo = MyRepository()
                repo.setKey(key)
                repo.setInitials(name, owner, watchers, forks)

                #check here if repo dont exist already in dictionary!
                if key in repos:
                    scream.log('We already found rep ' + key +
                               ' in the dictionary..')
                else:
                    repos[key] = repo

    scream.say('Finished creating dictionary, size of dict is: ' +
               str(len(repos)))

    for key in repos:
        repo = repos[key]

        try:
            repository = gh.get_repo(repo.getKey())
        except GithubException.UnknownObjectException as e:
            scream.log('Repo with key + ' + key +
                       ' not found, error({0}): {1}'.
                       format(e.errno, e.strerror))

        'getting languages of a repo'
        languages = repository.get_languages()  # dict object (json? object)
        repo.setLanguage(languages)
        scream.log('Added languages ' + str(languages) + ' to a repo ' + key)

        'getting labels, label is a tag which you can put in an issue'
        labels = repository.get_labels()  # github.Label object
        repo_labels = []
        for label in labels:
            repo_labels.append(label)
        repo.setLabels(repo_labels)
        scream.log('Added labels of count: ' + str(len(repo_labels)) +
                   ' to a repo ' + key)

        'getting repo branches'
        branches = repository.get_branches()
        repo_branches = []
        for branch in branches:
            repo_branches.append(branch)
        repo.setBranches(repo_branches)
        scream.log('Added branches of count: ' + str(len(repo_branches)) +
                   ' to a repo ' + key)

        scream.ssay('Finished processing repo: ' + key + '.. moving on... ')
