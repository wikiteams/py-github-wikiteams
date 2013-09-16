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


class MyDialect(csv.Dialect):
    strict = True
    skipinitialspace = True
    quoting = csv.QUOTE_NONE
    delimiter = ','
    lineterminator = '\n'


def make_headers():
    with open('repos.csv', 'ab') as output_csvfile:
        repowriter = csv.writer(output_csvfile, dialect=MyDialect)
        tempv = ('name', 'owner', 'forks_count', 'watchers_count',
                 'contributors_count', 'subscribers_count', 'stargazers_count')
        repowriter.writerow(tempv)


def output_data(repo):
    with open('repos.csv', 'ab') as output_csvfile:
        scream.ssay('repos.csv opened for append..')
        repowriter = csv.writer(output_csvfile, dialect=MyDialect)
        tempv = (repo.getName(),
                 repo.getOwner(),
                 repo.getForksCount(),
                 repo.getWatchersCount(),
                 repo.getContributorsCount(),
                 repo.getSubscribersCount(),
                 repo.getStargazersCount())
        repowriter.writerow(tempv)

    with open('contributors.csv', 'ab') as output_csvfile:
        scream.ssay('contributors.csv opened for append..')
        contribwriter = csv.writer(output_csvfile, dialect=MyDialect)
        for contributor in repo.getContributors():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     contributor.login)
            contribwriter.writerow(tempv)

    with open('languages.csv', 'ab') as output_csvfile:
        scream.ssay('languages.csv opened for append..')
        langwriter = csv.writer(output_csvfile, dialect=MyDialect)
        for language in repo.getLanguages():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     language)
            langwriter.writerow(tempv)

    with open('subscribers.csv', 'ab') as output_csvfile:
        scream.ssay('subscribers.csv opened for append..')
        subscriberswriter = csv.writer(output_csvfile, dialect=MyDialect)
        for subscriber in repo.getContributors():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     subscriber.login)
            subscriberswriter.writerow(tempv)


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

    make_headers()

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

        '1. Rozmiar zespolu'
        contributors = repository.get_contributors()
        repo_contributors = []
        for contributor in contributors:
            repo_contributors.append(contributor)
        repo.setContributors(repo_contributors)
        #repo.setContributorsCount(len(repo_contributors))
        'class fields are not garbage, its better to calculate count on demand'
        scream.log('Added contributors of count: ' +
                   str(len(repo_contributors)) +
                   ' to a repo ' + key)

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

        '2. Liczba commit'
        commits = repository.get_commits()
        repo_commits = []
        for commit in commits:
            repo_commits.append(commit)
        repo.setCommits(repo_commits)
        scream.log('Added commits of count: ' + str(len(repo_commits)) +
                   ' to a repo ' + key)

        '4. Liczba gwiazdek  (to zostanie uzyte jako jakosc zespolu)'
        stargazers = repository.get_stargazers()
        repo_stargazers = []
        for stargazer in stargazers:
            repo_stargazers.append(stargazer)
        repo.setStargazers(repo_stargazers)
        scream.log('Added stargazers of count: ' + str(len(repo_stargazers)) +
                   ' to a repo ' + key)

        '6. Liczba Issues w poszczegolnych typach'
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

        'get subscribers'
        subscribers = repository.get_subscribers()
        repo_subscribers = []
        for subscriber in subscribers:
            repo_subscribers.append(subscriber)
        repo.setSubscribers(repo_subscribers)
        scream.log('Added subscribers of count: ' +
                   str(len(repo_subscribers)) +
                   ' to a repo ' + key)

        scream.say('Persisting a repo to CSV output...')

        'handle here writing to output, dont make it at end when stack'
        'is full of repos, but do it a repo by repo...'
        output_data(repo)

        scream.ssay('Finished processing repo: ' + key + '.. moving on... ')

        del repos[key]

        scream.ssay('(' + key + ' deleted)')

        limit = gh.get_rate_limit()

        scream.ssay('Rate limit: ' + str(limit.rate.limit) +
                    ' remaining: ' + str(limit.rate.remaining))
