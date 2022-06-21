# Необходимые импорты
import json
from flask_restful import Resource
from flask.json import jsonify
from flask import make_response, request
from sqlalchemy.orm import session
from module.auth.commands import AuthCommand
from errors.AuthErrors import PassMathError, PassNotCorrectError, UserNotFoundError, UserExistError


class RegRoute(Resource):
    def __init__(self):
        self.authCommand = AuthCommand()
        
    def post(self):
        body = json.loads(request.data.decode())
        mail = body['mail'].strip()
        login = body['login'].strip()
        password = body['password']
        repeat_password = body['repeat_password']
        name = body['name'].strip()
        if mail == '' or login == '' or name == '' or len(password) < 6:
            return 'Date not correct', 401
        try:
            new_user, token = self.authCommand.registration(mail, login, password, repeat_password, name)
        except PassMathError:
            return 'Password not math', 401
        except UserExistError:
            return 'User is exist', 401
        print(new_user.__dict__)
        response = make_response(jsonify(new_user.__dict__))
        response.set_cookie('session', token)
        return response


class LoginRoute(Resource):
    def __init__(self):
        self.authCommand = AuthCommand()
        
    def post(self):
        body = json.loads(request.data.decode())
        login = body['login']
        password = body['password']
        try:
            token = self.authCommand.login(login, password)
        except UserNotFoundError:
            return 'User not found', 400
        except PassNotCorrectError:
            return 'Password not correct', 400
        response = make_response(jsonify({}))
        response.set_cookie('new_session', token)
        return response


class LogoutRoute(Resource):
    def __init__(self):
        self.authCommand = AuthCommand()
        
    def get(self):
        token = self.authCommand.logout()
        response = make_response(jsonify({}))
        response.set_cookie('new_session', token)
        return response
