'''
WikiTeams.pl top 32000 repos dataset creator
Please keep this file with PEP8 standard
Dont fork without good reason, use clone instead

@since 1.2
@author Oskar Jarczyk

@update 18.09.2013
'''

version_name = 'version 1.2 codename: september'

from intelliRepository import MyRepository
from github import Github, UnknownObjectException, GithubException
import csv
import scream
import gc
import sys
import codecs
import cStringIO

repos = dict()

'''
Explanation of an input data, theye are CSV file with data
retrieved from Google BigQuery consisted of repo name, owner
and sorted by number of forks and watchers, for analysis we
take around 32k biggest GitHub repositories
'''
file_names = ['by-forks-20028-33', 'by-forks-20028-44',
              'by-watchers-3391-118', 'by-watchers-129-82',
              'by-watchers-82-70']
repos_reported_nonexist = []

AUTH_WITH_TOKENS = False
USE_UTF8 = True


class MyDialect(csv.Dialect):
    strict = True
    skipinitialspace = True
    quoting = csv.QUOTE_MINIMAL
    delimiter = ','
    escapechar = '\\'
    quotechar = '"'
    lineterminator = '\n'


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=MyDialect, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def make_headers():
    with open('repos.csv', 'ab') as output_csvfile:
        repowriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        tempv = ('name', 'owner', 'forks_count', 'watchers_count',
                 'contributors_count', 'subscribers_count',
                 'stargazers_count', 'labels_count', 'commits_count')
        repowriter.writerow(tempv)


def output_commit_comments(commit_comments, sha):
    with open('commit_comments.csv', 'ab') as output_csvfile:
        scream.log('commit_comments.csv opened for append..')
        ccomentswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for comment in commit_comments:
            assert (type(comment.id) == int or comment.id is None)
            assert (type(comment.position) == int or comment.position is None)
            assert (type(comment.line) == int or comment.line is None)
            scream.log(str(comment.commit_id))
            tempv = (repo.getName(),
                     repo.getOwner(),
                     sha,
                     (comment.body.strip('\r').strip('\n') if comment.body is not None else ''),
                     (str(comment.commit_id) if comment.commit_id is not None else ''),  # logged above
                     (str(comment.created_at) if comment.created_at is not None else ''),
                     (str(comment.id) if comment.id is not None else ''),  # this is always int
                     (str(comment.line) if comment.line is not None else ''),  # this is always int
                     (comment.path if comment.path is not None else ''),
                     (str(comment.position) if comment.position is not None else ''),  # this is always int
                     (str(comment.updated_at) if comment.updated_at is not None else ''))
            ccomentswriter.writerow(tempv)


def output_commit_statuses(commit_statuses, sha):
    with open('commit_statuses.csv', 'ab') as output_csvfile:
        scream.log('commit_statuses.csv opened for append..')
        cstatuswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for status in commit_statuses:
            tempv = (repo.getName(),
                     repo.getOwner(),
                     sha,
                     (str(status.created_at) if status.created_at is not None else ''),
                     (status.creator.login if status.creator is not None else ''),
                     (status.description if status.description is not None else ''),
                     (str(status.id) if status.id is not None else ''),
                     (status.state if status.state is not None else ''),
                     (str(status.updated_at) if status.updated_at is not None else ''))
            cstatuswriter.writerow(tempv)


def output_commit_stats(commit_stats, sha):
    with open('commit_stats.csv', 'ab') as output_csvfile:
        scream.log('commit_stats.csv opened for append..')
        cstatswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        assert (type(commit_stats.additions) == int or commit_stats.additions is None)
        assert (type(commit_stats.deletions) == int or commit_stats.deletions is None)
        assert (type(commit_stats.total) == int or commit_stats.total is None)
        tempv = (repo.getName(),
                 repo.getOwner(),
                 sha,
                 (str(commit_stats.additions) if commit_stats.additions is not None else ''),  # this is always int ! str() allowed
                 (str(commit_stats.deletions) if commit_stats.deletions is not None else ''),  # this is always int ! str() allowed
                 (str(commit_stats.total) if commit_stats.total is not None else ''))  # this is always int ! str() allowed
        cstatswriter.writerow(tempv)


def output_data(repo):
    with open('repos.csv', 'ab') as output_csvfile:
        scream.ssay('repos.csv opened for append..')
        repowriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)

        rfc = repo.getForksCount()
        rwc = repo.getWatchersCount()
        rcc = repo.getContributorsCount()
        rsc = repo.getSubscribersCount()
        rstc = repo.getStargazersCount()
        rlc = repo.getLabelsCount()
        rcmc = repo.getCommitsCount()
        rpc = repo.getPullsCount()
        assert rfc.isdigit()
        assert rwc.isdigit()
        assert type(rcc) == int
        assert type(rsc) == int
        assert type(rstc) == int
        assert type(rlc) == int
        assert type(rcmc) == int
        assert type(rpc) == int

        tempv = (repo.getName(),
                 repo.getOwner(),
                 str(rfc),  # this is always string representation of number ! str() allowed
                 str(rwc),  # this is always string representation of number ! str() allowed
                 str(rcc),  # this is always int ! str() allowed
                 str(rsc),  # this is always int ! str() allowed
                 str(rstc),  # this is always int ! str() allowed
                 str(rlc),  # this is always int ! str() allowed
                 str(rcmc),  # this is always int ! str() allowed
                 str(rpc))  # this is always int ! str() allowed
        repowriter.writerow(tempv)

    with open('contributors.csv', 'ab') as output_csvfile:
        scream.ssay('contributors.csv opened for append..')
        contribwriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for contributor in repo.getContributors():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     contributor.login)
            contribwriter.writerow(tempv)

    with open('commits.csv', 'ab') as output_csvfile:
        scream.ssay('commits.csv opened for append..')
        commitswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for commit in repo.getCommits():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     commit.sha,
                     (commit.author.login if commit.author is not None else ''),
                     (commit.committer.login if commit.committer is not None else ''),
                     commit.url,
                     commit.html_url)
            commitswriter.writerow(tempv)

    with open('languages.csv', 'ab') as output_csvfile:
        scream.ssay('languages.csv opened for append..')
        langwriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for language in repo.getLanguages():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     language)
            langwriter.writerow(tempv)

    with open('subscribers.csv', 'ab') as output_csvfile:
        scream.ssay('subscribers.csv opened for append..')
        subscriberswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for subscriber in repo.getContributors():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     subscriber.login)
            subscriberswriter.writerow(tempv)

    with open('labels.csv', 'ab') as output_csvfile:
        scream.ssay('labels.csv opened for append..')
        labelswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for label in repo.getLabels():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     label.name,
                     label.color)
            labelswriter.writerow(tempv)

    with open('issues.csv', 'ab') as output_csvfile:
        scream.ssay('issues.csv opened for append..')
        issueswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for issue in repo.getIssues():
            assert (type(issue.id) == int or issue.id is None)
            assert (type(issue.number) == int or issue.number is None)
            tempv = (repo.getName(),
                     repo.getOwner(),
                     (issue.assignee.login if issue.assignee is not None else ''),
                     (issue.body.strip('\r').strip('\n') if issue.body is not None else ''),
                     (issue.closed_at if issue.closed_at is not None else ''),
                     (issue.closed_by.login if issue.closed_by is not None else ''),
                     str(issue.id),
                     str(issue.number),
                     (issue.title if issue.title is not None else ''))
            issueswriter.writerow(tempv)

    with open('pulls.csv', 'ab') as output_csvfile:
        scream.ssay('pulls.csv opened for append..')
        pullswriter = UnicodeWriter(output_csvfile) if USE_UTF8 else csv.writer(output_csvfile, dialect=MyDialect)
        for pull in repo.getPulls():
            tempv = (repo.getName(),
                     repo.getOwner(),
                     str(pull.additions),  # is always int
                     (pull.assignee.login if pull.assignee is not None else ''),
                     (pull.body if pull.body is not None else ''),
                     str(pull.changed_files),  # is always int
                     (str(pull.closed_at) if pull.closed_at is not None else ''),
                     str(pull.comments),  # is always int
                     pull.comments_url,
                     (str(pull.created_at) if pull.created_at is not None else ''),
                     str(pull.deletions),  # is always int
                     pull.diff_url,
                     pull.html_url,
                     str(pull.id),  # is always int
                     pull.issue_url,
                     pull.merge_commit_sha,
                     str(pull.mergeable),  # is always boolean
                     pull.mergeable_state,
                     str(pull.merged),  # is always boolean
                     (str(pull.merged_at) if pull.merged_at is not None else ''),
                     str(pull.number),
                     pull.patch_url,
                     pull.review_comment_url,
                     str(pull.review_comments),  # is always int
                     pull.review_comments_url,
                     pull.state,
                     pull.title,
                     (str(pull.updated_at) if pull.updated_at is not None else ''),
                     (pull.user.login if pull.user is not None else ''))
            pullswriter.writerow(tempv)


if __name__ == "__main__":
    '''
    Starts process of work on CSV files which are output of google bigquery
    whenever intelli_git.py is executed as an standalone program
    '''
    scream.say('Start main execution')
    scream.say('Welcome to WikiTeams.pl GitHub repo getter!')
    scream.say(version_name)

    secrets = []
    with open('pass.txt', 'r') as passfile:
        for line in passfile:
            secrets.append(line)
    login_or_token__ = str(secrets[0]).strip()
    pass_string = str(secrets[1]).strip()
    client_id__ = str(secrets[2]).strip()
    client_secret__ = str(secrets[3]).strip()

    if AUTH_WITH_TOKENS:
        gh = Github(client_id=client_id__, client_secret=client_secret__)
    else:
        #print login_or_token__
        #print pass_string
        gh = Github(login_or_token__, pass_string)

    is_gc_turned_on = 'turned on' if str(gc.isenabled()) else 'turned off'
    scream.ssay('Garbage collector is ' + is_gc_turned_on)

    make_headers()

    for filename in file_names:
        scream.say('------ WORKING WITH FILE : ' + filename)
        filename_ = 'data/' if sys.platform == 'linux2' else 'data\\'
        filename__ = filename_ + filename + '.csv'
        with open(filename__, 'rb') as source_csvfile:
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

    iteration_step_count = 0

    for key in repos:
        repo = repos[key]

        try:
            repository = gh.get_repo(repo.getKey())
        except UnknownObjectException as e:
            scream.log_warning('Repo with key + ' + key +
                       ' not found, error({0}): {1}'.
                       format(e.status, e.data))
            repos_reported_nonexist.append(key)
            continue

        iteration_step_count += 1
        scream.ssay('Step no ' + str(iteration_step_count) + '. Working on a repo: ' + key)

        scream.ssay('Checking size of a team')
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

        scream.ssay('Getting languages of a repo')
        languages = repository.get_languages()  # dict object (json? object)
        repo.setLanguage(languages)
        scream.log('Added languages ' + str(languages) + ' to a repo ' + key)

        scream.ssay('Getting labels of a repo')
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
            if 'repo_labels' not in locals():
                repo.setLabels([])
            else:
                repo.setLabels(repo_labels)
            scream.log_error('Repo didnt gave any labels, or paginated through' +
                       ' labels gave error. Issues are disabled for this' +
                       ' repo? + ' + key +
                       ', error({0}): {1}'.
                       format(e.status, e.data))

        scream.ssay('Getting commits of a repo')
        '2. Liczba commit'
        try:
            commits = repository.get_commits()
            repo_commits = []
            for commit in commits:
                repo_commits.append(commit)
                comments = commit.get_comments()
                commit_comments = []
                for comment in comments:
                    commit_comments.append(comment)
                statuses = commit.get_statuses()
                commit_statuses = []
                for status in statuses:
                    commit_statuses.append(status)
                'IMHO output to CSV already here...'
                output_commit_comments(commit_comments, commit.sha)
                output_commit_statuses(commit_statuses, commit.sha)
                output_commit_stats(commit.stats, commit.sha)
            repo.setCommits(repo_commits)
            scream.log('Added commits of count: ' + str(len(repo_commits)) +
                       ' to a repo ' + key)
        except GithubException as e:
            if 'repo_commits' not in locals():
                repo.setCommits([])
            scream.log_error('Paginating through comments, comment comments or statuses' +
                       ' gave error. Try again? ' + key +
                       ', error({0}): {1}'.
                       format(e.status, e.data))

        '3. Liczba Commit w poszczegolnych skill (wiele zmiennych)'
        'there is no evidence for existance in GitHub API'
        'of a function for getting skill stats in a commit'
        'TO DO: implement a workaround with BEAUTIFUL SOUP'

        scream.ssay('Getting stargazers of a repo')
        '4. Liczba gwiazdek  (to zostanie uzyte jako jakosc zespolu)'
        stargazers = repository.get_stargazers()
        repo_stargazers = []
        for stargazer in stargazers:
            repo_stargazers.append(stargazer)
        repo.setStargazers(repo_stargazers)
        scream.log('Added stargazers of count: ' + str(len(repo_stargazers)) +
                   ' to a repo ' + key)

        scream.ssay('Getting issues of a repo')
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

        scream.ssay('Getting pull requests of a repo')
        '10. Liczba Pull Requests'
        '11. Liczba zaakceptowanych Pull Requests'
        pulls = repository.get_pulls()
        repo_pulls = []
        for pull in pulls:
            repo_pulls.append(pull)
        repo.setPulls(repo_pulls)
        scream.log('Added pulls of count: ' + str(len(repo_pulls)) +
                   ' to a repo ' + key)

        scream.ssay('Getting branches of a repo')
        'getting repo branches'
        '13. Liczba Branch'
        branches = repository.get_branches()
        repo_branches = []
        for branch in branches:
            repo_branches.append(branch)
        repo.setBranches(repo_branches)
        scream.log('Added branches of count: ' + str(len(repo_branches)) +
                   ' to a repo ' + key)

        scream.ssay('Getting subscribers of a repo')
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

        #del repos[key]
        'Dictionary cannot change size during iteration'
        'TO DO: associated fields purge so GC will finish the job'
        'implement reset() in intelliRepository.py'
        #scream.ssay('(' + key + ' deleted)')

        limit = gh.get_rate_limit()

        scream.ssay('Rate limit: ' + str(limit.rate.limit) +
                    ' remaining: ' + str(limit.rate.remaining))

        reset_time = gh.rate_limiting_resettime

        scream.ssay('Rate limit reset time: ' + str(reset_time))
