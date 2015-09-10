# -*- coding: utf-8 -*-

import json

import os

from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from ipa.collection import Collection
from ipa.auth import OAuth1

# Set these enviroment variables to access the resource's API
CLIENT_KEY = os.environ.get('CLIENT_KEY')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
RESOURCE_OWNER_KEY = os.environ.get('RESOURCE_OWNER_KEY')
RESOURCE_OWNER_SECRET = os.environ.get('RESOURCE_OWNER_SECRET')


Base = declarative_base()


class Business(Base):
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(String)
    
    def decode(self, response):
        return parse_repo(json.loads(response.body))

    def __repr__(self):
        return 'Business({}/{})'.format(self.name, self.rating)


class Businesses(Collection):
    table = Business

    def __init__(self, *args, **kwargs):
        super(Businesses, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return 'http://api.yelp.com/v2/search/'

    def decode(self, response):
        businesses = json.loads(response.body).get(self.__class__.__name__.lower())
        return [parse_repo(r) for r in businesses]


def parse_repo(raw):
    return {
        'id': raw['id'],
        'name': raw['name'],
        'rating': raw['rating']
    }


def main():

    term, location, search_limit = 'dinner', 'Chattanooga, TN', 3
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ','+'),
        'limit' : search_limit
    }

    def on_repos(repos, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for repo in repos:
            print repo

    auth = OAuth1(client_key=CLIENT_KEY,
                  client_secret=CLIENT_SECRET,
                  resource_owner_key=RESOURCE_OWNER_KEY,
                  resource_owner_secret=RESOURCE_OWNER_SECRET,
    )

    AsyncHTTPClient.configure(None, defaults=dict(user_agent="ipa-agent"))
    buss = Businesses(AsyncHTTPClient())
    buss.all(on_repos, auth=auth, url_params=url_params)

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
