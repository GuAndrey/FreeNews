from cgitb import reset
import json
from flask_restful import Resource
from flask.json import jsonify
from flask import make_response, request
from errors.ContentErrors import NoContentError
from module.comment.commands import CommentCommand
from errors.AuthErrors import AuthenticationError


class CommentRoute(Resource):
    def __init__(self):
        self.commentCommand = CommentCommand()
        
    def get(self, id):
        news_id = id
        comment = self.commentCommand.getCommentsListByNewsId(news_id, request.cookies)
        response = make_response(jsonify(list(map(lambda x: x.__dict__, comment))))
        return response
        
    def post(self, id):
        news_id = id
        body = json.loads(request.data.decode())
        content = body['content']
        try:
            new_news = self.commentCommand.addComment(content, news_id, request.cookies)
        except AuthenticationError:
            return "You don't write this comment", 403
        except NoContentError:
            return 'No comment', 404
        response = make_response(jsonify(new_news.__dict__))
        return response
        
    def delete(self, id):
        comment_id = id
        try:
            self.commentCommand.deleteComment(comment_id, request.cookies)
        except AuthenticationError:
            return "You don't write this comment", 403
        except NoContentError:
            return 'Not found comment', 404
        return 'Comment deleted', 200