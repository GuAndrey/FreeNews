from flask_restful import Resource
from flask.json import jsonify
from flask import request
from errors.AuthErrors import AuthenticationError
from module.stat.commands import StatCommand


class BaseStatRoute(Resource):
    def __init__(self):
        self.statCommand = StatCommand()
        

class LikeRoute(BaseStatRoute):
    def get(self, news_id):
        try:
            res = self.statCommand.swapLike(news_id, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 403
        return res
        

class RepRoute(BaseStatRoute):
    def get(self, news_id):
        try:
            res = self.statCommand.swapRep(news_id, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 403
        return res
        

class ViewRoute(BaseStatRoute):
    def get(self, news_id):
        try:
            res = self.statCommand.addView(news_id, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 403
        return res
        

class FavoriteRoute(BaseStatRoute):
    def get(self, news_id):
        try:
            res = self.statCommand.swapFavorite(news_id, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 403
        return res
        

class SubRoute(BaseStatRoute):
    def get(self, sub_id):
        try:
            res = self.statCommand.swapSubscribe(sub_id, request.cookies)
        except AuthenticationError:
            return AuthenticationError.__doc__, 403
        return res