'''
Represents a GitHub repository

@since 1.0
@author Oskar Jarczyk
'''


class MyRepository():

    element_type = 'Team'
    key = None

    def __init__(self):
        self.data = []

    repository_branches = None
    repository_commits = None
    repository_contributors = None
    repository_created_at = None
    repository_description = None
    repository_fork = None
    repository_forks = None
    repository_forks_count = None
    repository_has_downloads = None
    repository_has_issues = None
    repository_has_wiki = None
    repository_homepage = None
    repository_integrate_branch = None
    repository_issues = None
    repository_labels = None
    repository_language = None
    repository_master_branch = None
    repository_name = None
    repository_open_issues = None
    repository_organization = None
    repository_owner = None
    repository_private = None
    repository_pulls = None
    repository_pushed_at = None
    repository_size = None
    repository_stargazers = None
    repository_subscribers = None
    repository_watchers = None
    repository_url = None

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    'basicly first init of data transcripted from input (csvs)'
    'name with owner, and count of forks and watchers'
    def setInitials(self, name, owner, watchers, forks):
        self.repository_name = name
        self.repository_owner = owner
        self.repository_watchers_count = watchers
        self.repository_forks_count = forks

    def setName(self, name):
        self.repository_name = name

    def getName(self):
        return self.repository_name

    def setOwner(self, owner):
        self.repository_owner = owner

    def getOwner(self):
        return self.repository_owner

    def setForks(self, forks):
        self.repository_forks = forks

    def setCommits(self, commits):
        self.repository_commits = commits

    def getForks(self):
        return self.repository_forks

    def getForksCount(self):
        return self.repository_forks_count

    def setWatchers(self, watchers):
        self.repository_watchers = watchers

    def getWatchers(self):
        return self.repository_watchers

    def getWatchersCount(self):
        return self.repository_watchers_count

    def setContributors(self, contributors):
        self.repository_contributors = contributors

    def getContributors(self):
        return self.repository_contributors

    def getContributorsCount(self):
        return len(self.repository_contributors)

    def setSubscribers(self, subscribers):
        self.repository_subscribers = subscribers

    def getSubscribers(self,):
        return self.repository_subscribers

    def getSubscribersCount(self):
        return len(self.repository_subscribers)

    def setStargazers(self, stargazers):
        self.repository_stargazers = stargazers

    def getStargazers(self):
        return self.repository_stargazers

    def getStargazersCount(self):
        return len(self.repository_stargazers)

    def setLanguage(self, languages):
        self.repository_language = languages

    def setLabels(self, labels):
        self.repository_labels = labels

    def getLabels(self):
        return self.repository_labels

    def getLabelsCount(self):
        return len(self.repository_labels)

    def setIssues(self, issues):
        self.repository_issues = issues

    def getIssues(self):
        return self.repository_issues

    def getIssuesCount(self):
        return len(self.repository_issues)

    def setBranches(self, branches):
        self.repository_branches = branches

    def setPulls(self, pulls):
        self.repository_pulls = pulls

    def getLanguages(self):
        return self.repository_language
