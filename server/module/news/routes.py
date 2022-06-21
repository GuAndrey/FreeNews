import json
import re
from flask_restful import Resource
from flask.json import jsonify
from errors.AuthErrors import AuthenticationError
from errors.ContentErrors import NoContentError
from module.news.commands import NewsCommand
from flask import make_response, request
from module.news.vo import CATEGORYS, REGIONS


class BaseNewsRoute(Resource):
    def __init__(self):
        self.newsCommand = NewsCommand()
        

class NewsRoute(BaseNewsRoute):
    def get(self, news_id):
        try:
            news = self.newsCommand.getOneNews(news_id, request.cookies)
        except AuthenticationError:
            return "News not approved", 403
        except NoContentError:
            return 'Not found News', 404
        response = make_response(jsonify(news.__dict__))
        return response
        
    def delete(self, news_id):
        try:
            self.newsCommand.deleteNews(news_id, request.cookies)
        except AuthenticationError:
            return "You don't write this news", 403
        except NoContentError:
            return 'Not found News', 404
        return 'Comment deleted', 200
        
    def post(self):
        body = json.loads(request.data.decode())
        title = body['title']
        content = body['content']
        region = body['region']
        category = body['category']
        try:
            new_news = self.newsCommand.addNews(title, content, region, category, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 401
        response = make_response(jsonify(new_news.__dict__))
        return response


class NewsResourceRoute(BaseNewsRoute):
    def post(self, news_id):
        try:
            self.newsCommand.addNewsResourse(request.files.get('image'), news_id, request.cookies)
        except AuthenticationError:
            return "You don't write this news", 403
        except NoContentError:
            return 'Not found News', 404
        except AttributeError:
            return 'Resourse not pass', 404
        return 'Resourse added', 200
        

class NewsListRoute(BaseNewsRoute):
    def get(self):
        newsList = self.newsCommand.getNewsList(request.cookies)
        return jsonify(list(map(lambda x: x.__dict__, newsList)))
        
    def post(self):
        body = json.loads(request.data.decode())
        author_id = body.get('author_id')
        if author_id:
            newsList = self.newsCommand.getNewsListByAuthor(author_id, request.cookies)
            return jsonify(list(map(lambda x: x.__dict__, newsList)))
        newsList = self.newsCommand.getNewsList(body, request.cookies)
        return jsonify(list(map(lambda x: x.__dict__, newsList)))
        

class NewsCategoryRoute(Resource):
    def get(self):
        return CATEGORYS
        
        
class NewsRegionRoute(Resource):
    def get(self):
        return REGIONS