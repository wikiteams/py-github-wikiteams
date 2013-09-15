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

    repository_url = None
    repository_has_downloads = None
    repository_created_at = None
    repository_has_issues = None
    repository_description = None
    repository_forks = None
    repository_fork = None
    repository_has_wiki = None
    repository_homepage = None
    repository_size = None
    repository_private = None
    repository_name = None
    repository_owner = None
    repository_open_issues = None
    repository_watchers = None
    repository_pushed_at = None
    repository_language = None
    repository_organization = None
    repository_integrate_branch = None
    repository_master_branch = None

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def setInitials(self, name, owner, watchers, forks):
        self.repository_name = name
        self.repository_owner = owner
        self.repository_watchers = watchers
        self.repository_forks = forks

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

    def setWatchers(self, watchers):
        self.repository_watchers = watchers

    def setLanguage(self, languages):
        self.repository_language = languages

    def getLanguages(self):
        return self.repository_language
