# -*- coding: utf-8 -*-

import json

from ipa.collection import Collection

from tornado import httpclient, ioloop

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Repo(Base):
    __tablename__ = 'repos'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(String)
    is_private = Column(String)

    def decode(self, response):
        return parse_repo(json.loads(response.body))

    def __repr__(self):
        return 'Repo({}/{})'.format(self.owner, self.name)


class Repos(Collection):
    table = Repo

    def __init__(self, username, *args, **kwargs):
        self.username = username

        super(Repos, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return 'https://api.github.com/users/{}/repos'.format(self.username)

    def decode(self, response):
        return [parse_repo(r) for r in json.loads(response.body)]


def parse_repo(raw):
    return {
        'id': raw['id'],
        'name': raw['name'],
        'owner': raw['owner']['login'],
        'is_private': raw['private']
    }


def main():
    def on_repos(repos, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for repo in repos:
            import ipdb; ipdb.set_trace()
            print repo

    repos = Repos('jaimegildesagredo', httpclient.AsyncHTTPClient(force_instance=True, defaults=dict(user_agent='myagent')))
    repos.all(on_repos)

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
