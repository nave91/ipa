
try:
    from http.client import BAD_REQUEST, HTTPException
except ImportError:
    from httplib import BAD_REQUEST, HTTPException
try:
    from urllib.parse import splitquery
except ImportError:
    from urllib import splitquery

from functools import partial

from tornado import escape, httputil
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from auth import OAuth1

class Collection(object):
    table = None

    def __init__(self, client):
        self.client = client

    def all(self, callback, **kwargs):
        self.request_all(callback, **kwargs)

    def request_all(self, callback, auth=None, url_params=None):
        url = self.url
        if url_params:
            url = httputil.url_concat(url, url_params)
        if isinstance(self.client, AsyncHTTPClient):
            request = HTTPRequest(url)
        else:
            request = url
        if auth:
            auth(request)
        self.client.fetch(request, callback=partial(self.on_query, callback))

    def query(self, params, callback):
        self.request_query(callback, params)

    def request_query(self, params, callback):
        self.client.fetch(self.url, params=params, callback=partial(self.on_query, callback))

    def on_query(self, callback, response):
        
        if response.code >= BAD_REQUEST:
            raise HTTPException(response.code)
        
        if hasattr(self, 'decode'):
            collection = self.decode(response)
        else:
            collection = escape.json_decode(response.body)

        if not isinstance(collection, list):
            callback(None, ValueError("""
                The response body was expected to be a JSON array.

                To properly process the response you should define a
                `decode(response)` method in your `Collection` class."""))

            return

        result = []

        try:
            for r in collection:
                obj = self.table(**r)
                result.append(obj)
        except Exception as error:
            callback(None, error)
        else:
            callback(result, None)

    def get(self, id_, callback, **kwargs):
        self.request_get(id_, callback, **kwargs)

    def request_get(self, id_, callback, auth=None, url_params=None):
        url= self._url(id_)
        if url_params:
            url = httputil.url_concat(url, url_params)
        if isinstance(self.client, AsyncHTTPClient):
            request = HTTPRequest(url)
        else:
            request = url
        if auth:
            auth(request)
        self.client.fetch(request, callback=partial(self.on_get, callback))

    def on_get(self, callback, response):
        
        if response.code >= BAD_REQUEST:
            raise HTTPException

        if hasattr(result, 'decode'):
            item = result.decode(response)
        else:
            item = escape.json_decode(response.body)

        try:
            result = self.table(**item)
        except Exception as error:
            callback(None, error)
        else:
            callback(result, None)

    def _url(self, obj_or_id):
        if isinstance(obj_or_id, self.table):
            id_ = self._id(obj_or_id)
            url = getattr(obj_or_id, '_url', self.url)
        else:
            id_ = obj_or_id
            url = getattr(self.table, '_url', self.url)

        if callable(url):
            return url(id_)

        url, query = splitquery(url)

        url = '{}/{}'.format(url, id_)

        if query is not None:
            url = '{}?{}'.format(url, query)

        return url

    def _id(self, obj):
        for field in obj.__table__.columns:
            if field.primary_key:
                return obj.__dict__.get(field.name)

