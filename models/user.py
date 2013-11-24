import psycopg2
from lib.db import Database

class User():
    @staticmethod
    def add_or_update(data):
        db = Database()
        db.connection.autocommit = True
        cur = db.connection.cursor()

        try:
            ghData = {
                'id': data.id,
                'login': data.login,
                'name': data.name,
                'type': data.type,
                'email': data.email,
                'location': data.location,
                'company': data.company,
                'bio': data.bio,
                'blog': data.blog,
                'disk_usage': data.disk_usage,
                'gravatar_id': data.gravatar_id,
                'hireable': data.hireable,

                'followers': data.followers,
                'following': data.following,

                'collaborators': data.collaborators,
                'contributions': data.contributions,

                'public_repos': data.public_repos,
                'owned_private_repos': data.owned_private_repos,
                'total_private_repos': data.total_private_repos,

                'public_gists': data.public_gists,
                'private_gists': data.private_gists,

                'url': data.url,
                'avatar_url': data.avatar_url,
                'events_url': data.events_url,
                'followers_url': data.followers_url,
                'following_url': data.following_url,
                'gists_url': data.gists_url,
                'html_url': data.html_url,
                'organizations_url': data.organizations_url,
                'received_events_url': data.received_events_url,
                'repos_url': data.repos_url,
                'starred_url': data.starred_url,
                'subscriptions_url': data.subscriptions_url,

                'created_at': data.created_at,
                'updated_at': data.updated_at,

                #'plan': data.plan,
            }

            sql = "INSERT INTO public.users (id, login, name, type, email, location, company, bio, blog, disk_usage, " \
                  "gravatar_id, hireable, followers, following, collaborators, contributions, public_repos, " \
                  "owned_private_repos, total_private_repos, public_gists, private_gists, url, avatar_url, events_url, " \
                  "followers_url, following_url, gists_url, html_url, organizations_url, received_events_url, repos_url, " \
                  "starred_url, subscriptions_url, created_at, updated_at)" \
                  "VALUES (%(id)s, %(login)s, %(name)s, %(type)s, %(email)s, %(location)s, %(company)s, %(bio)s, " \
                  "%(blog)s, %(disk_usage)s, %(gravatar_id)s, %(hireable)s, %(followers)s, %(following)s, " \
                  "%(collaborators)s, %(contributions)s, %(public_repos)s, %(owned_private_repos)s, " \
                  "%(total_private_repos)s, %(public_gists)s, %(private_gists)s, %(url)s, %(avatar_url)s, " \
                  "%(events_url)s, %(followers_url)s, %(following_url)s, %(gists_url)s, %(html_url)s, " \
                  "%(organizations_url)s, %(received_events_url)s, %(repos_url)s, %(starred_url)s, %(subscriptions_url)s, " \
                  "%(created_at)s, %(updated_at)s)"

            cur.execute(sql, ghData)
            db.connection.commit()
        except psycopg2.IntegrityError as err:
            print 'User exists!'

            sql = "UPDATE public.users SET " \
                  "login = %(login)s, " \
                  "name = %(name)s, " \
                  "type = %(type)s, " \
                  "email = %(email)s, " \
                  "location = %(location)s, " \
                  "company = %(company)s, " \
                  "bio = %(bio)s, " \
                  "blog = %(blog)s, " \
                  "disk_usage = %(disk_usage)s, " \
                  "gravatar_id = %(gravatar_id)s, " \
                  "hireable = %(hireable)s, " \
                  "followers = %(followers)s, " \
                  "following = %(following)s, " \
                  "collaborators = %(collaborators)s, " \
                  "contributions = %(contributions)s, " \
                  "public_repos = %(public_repos)s, " \
                  "owned_private_repos = %(owned_private_repos)s, " \
                  "total_private_repos = %(total_private_repos)s, " \
                  "public_gists = %(public_gists)s, " \
                  "private_gists = %(private_gists)s, " \
                  "url = %(url)s, " \
                  "avatar_url = %(avatar_url)s, " \
                  "events_url = %(events_url)s, " \
                  "followers_url = %(followers_url)s, " \
                  "following_url = %(following_url)s, " \
                  "gists_url = %(gists_url)s, " \
                  "html_url = %(html_url)s, " \
                  "organizations_url = %(organizations_url)s, " \
                  "received_events_url = %(received_events_url)s, " \
                  "repos_url = %(repos_url)s, " \
                  "starred_url = %(starred_url)s, " \
                  "subscriptions_url = %(subscriptions_url)s, " \
                  "created_at = %(created_at)s, " \
                  "updated_at = %(created_at)s " \
                  "WHERE id = %(id)s"

            cur.execute(sql, ghData)

        except Exception as err:
            print 'Error: '
            print err.message

        finally:
            sql = "SELECT * FROM public.users WHERE id = %(id)s"
            cur.execute(sql, ghData)

            dbContributor = cur.fetchone()

            return dbContributor