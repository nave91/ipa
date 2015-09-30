# -*- coding: utf-8 -*-

import json, os

from ipa.collection import Collection

from tornado import httpclient, ioloop

from sqlalchemy import Column, String, Integer, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SurveyResponse(Base):
    __tablename__ = 'survey_responses'

    id = Column(Integer, primary_key=True)
    person_name = Column(String)
    person_email = Column(String)
    person_id = Column(Integer)
    score = Column(Integer)
    comment = Column(NVARCHAR(10000))

    def decode(self, response):
        return parse_sresponses(json.loads(response.body))

    def __repr__(self):
        return 'SReponse({}/{})'.format(self.person_name, self.score)


class SurveyResponses(Collection):
    table = SurveyResponse

    @property
    def url(self):
        return 'https://api.delighted.com/v1/survey_responses.json'

    def decode(self, response):
        return [parse_response(r) for r in json.loads(response.body)]


def parse_response(survey_response):
    return {
        'id': survey_response['id'],
        'person_name': survey_response['person']['name'],
        'person_email': survey_response['person']['email'],
        'person_id': survey_response['person']['id'],
        'score': survey_response['score'],
        'comment': survey_response['comment']
        }


def main():
    def on_sresponses(repos, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for repo in repos:
            print repo

    import ipdb; ipdb.set_trace()
    API_KEY = os.environ.get('DELIGHTED_API_KEY')

    url_params = {
        'expand': 'person'
    }
    sresponses = SurveyResponses(httpclient.AsyncHTTPClient(force_instance=True, defaults=dict(user_agent='myagent')))
    sresponses.all(on_sresponses, req_kwargs={'auth_username':API_KEY}, url_params=url_params)

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
