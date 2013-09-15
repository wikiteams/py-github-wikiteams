'''
WikiTeams.pl top 32000 repos dataset creator
Please keep this file with PEP8 standard
Dont fork without good reason, use clone instead

@since 1.1
@author Oskar Jarczyk
'''

from intelliRepository import MyRepository
from github import Github, UnknownObjectException, GithubException
import csv
import scream
import gc

repos = dict()
file_names = ['by-forks-20028-33', 'by-forks-20028-44',
              'by-watchers-3391-118', 'by-watchers-129-82',
              'by-watchers-82-70']
repos_reported_nonexist = []

if __name__ == "__main__":
    '''
    Starts process of work on CSV files which are output of google bigquery
    whenever intelli_git.py is executed as an standalone program
    '''
    scream.say('start main')
    scream.say('Welcome to WikiTeams.pl GitHub repo getter!')

    pass_string = open('pass.txt', 'r').read()
    gh = Github('wikiteams', pass_string)

    scream.ssay('Garbage collector is ' + str(gc.isenabled()))

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

                '12. Liczba Fork'
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
        except UnknownObjectException as e:
            scream.log('Repo with key + ' + key +
                       ' not found, error({0}): {1}'.
                       format(e.status, e.data))
            repos_reported_nonexist.append(key)
            continue

        'getting languages of a repo'
        languages = repository.get_languages()  # dict object (json? object)
        repo.setLanguage(languages)
        scream.log('Added languages ' + str(languages) + ' to a repo ' + key)

        'getting labels, label is a tag which you can put in an issue'
        try:
            labels = repository.get_labels()  # github.Label object
            repo_labels = []
            for label in labels:
                repo_labels.append(label)
            repo.setLabels(repo_labels)
            scream.log('Added labels of count: ' + str(len(repo_labels)) +
                       ' to a repo ' + key)
        except GithubException as e:
            scream.log('Repo didnt gave any labels, or paginated through' +
                       ' labels gave error. Issues are disabled for this' +
                       ' repo? + ' + key +
                       ', error({0}): {1}'.
                       format(e.status, e.data))

        '4. Liczba gwiazdek  (to zostanie użyte jako jakość zespołu)'
        stargazers = repository.get_stargazers()
        repo_stargazers = []
        for stargazer in stargazers:
            repo_stargazers.append(stargazer)
        repo.setStargazers(repo_stargazers)
        scream.log('Added stargazers of count: ' + str(len(repo_stargazers)) +
                   ' to a repo ' + key)

        '6. Liczba Issues w poszczególnych typach'
        try:
            issues = repository.get_issues()
            repo_issues = []
            for issue in issues:
                repo_issues.append(issue)
            repo.setIssues(repo_issues)
            scream.log('Added issues of count: ' + str(len(repo_issues)) +
                       ' to a repo ' + key)
        except GithubException as e:
            scream.log('Repo didnt gave any issues, or paginated through' +
                       ' issues gave error. Issues are disabled for this' +
                       ' repo? + ' + key +
                       ', error({0}): {1}'.
                       format(e.status, e.data))

        '10. Liczba Pull Requests'
        '11. Liczba zaakceptowanych Pull Requests'
        pulls = repository.get_pulls()
        repo_pulls = []
        for pull in pulls:
            repo_pulls.append(pull)
        repo.setPulls(repo_pulls)
        scream.log('Added pulls of count: ' + str(len(repo_pulls)) +
                   ' to a repo ' + key)

        'getting repo branches'
        '13. Liczba Branch'
        branches = repository.get_branches()
        repo_branches = []
        for branch in branches:
            repo_branches.append(branch)
        repo.setBranches(repo_branches)
        scream.log('Added branches of count: ' + str(len(repo_branches)) +
                   ' to a repo ' + key)

        scream.say('Persisting a repo to CSV output...')

        'handle here writing to output, dont make it at end when stack'
        'is full of repos, but do it a repo by repo...'

        scream.ssay('Finished processing repo: ' + key + '.. moving on... ')
