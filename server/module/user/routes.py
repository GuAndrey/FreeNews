import json
from flask_restful import Resource
from flask.json import jsonify
from errors.AuthErrors import AuthenticationError
from module.user.commands import UserCommand
from flask import request


class BaseUserRoute(Resource):
    def __init__(self):
        self.userCommand = UserCommand()
        

class UserRoute(BaseUserRoute):
    def get(self, user_id):
        user = self.userCommand.getOneUser(user_id, request.cookies)
        return jsonify(user.__dict__)
        
    def put(self, user_id):
        body = json.loads(request.data.decode())
        description = body['description']
        try:
            user = self.userCommand.editUser(user_id, description, request.cookies)
        except AuthenticationError:
            return "You not this user", 403
        return jsonify(user.__dict__)
        

class UserListRoute(BaseUserRoute):
    def post(self):
        body = json.loads(request.data.decode())
        userList = self.userCommand.getUserList(body, request.cookies)
        return jsonify(list(map(lambda x: x.__dict__, userList)))
        

class UserCurretIdRoute(BaseUserRoute):
    def get(self):
        user_id = self.userCommand.getCurrentUserId(request.cookies)  
        return user_id
        

class UserAvatarRoute(BaseUserRoute):
    def post(self):
        try:
            self.userCommand.addUserAvatar(request.files.get('image'), request.cookies)
        except AuthenticationError:
            return "You not authentication", 403
        except AttributeError:
            return 'Avatar not pass', 404
        return 'Avatar added', 200
        
        
class UserSwapRoleRoute(BaseUserRoute):
    def get(self):
        try:
            user = self.userCommand.swapRole(request.cookies)
        except AuthenticationError:
            return "You not authentication", 403
        return jsonify(user.__dict__) 