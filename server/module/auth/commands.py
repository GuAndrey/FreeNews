from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from db.connection import ENGINE
from config.globals import PRIVATE_KEY
from models import User
from errors.AuthErrors import PassMathError, PassNotCorrectError, UserNotFoundError, UserExistError
from module.user.mapper import userToDto
import flask_login


class AuthCommand:
    
    def __init__(self):
        self.session = Session(bind=ENGINE)

    def __del__(self):
        self.session.close()
        
    def registration(self, email, login, password, repeat_password, name):
        if (password != repeat_password):
            raise PassMathError
        if (self.session.query(User).filter_by(login=login).first() or
            self.session.query(User).filter_by(email=email).first()):
            raise UserExistError
        pass_hash = generate_password_hash(str(password))
        user = User()
        user.password = pass_hash
        user.login = login
        user.email = email
        user.name = name
        user.role = 0
        user.avatar = 'http://dummyimage.com/207x100.png/ff4444/ffffff'
        self.session.add(user)
        self.session.commit()
        token = jwt.encode({"user_id": user.id}, PRIVATE_KEY, algorithm="HS256")
        return (userToDto(user, True), token)
        
    def login(self, login, password):
        user = self.session.query(User).filter_by(login=login).first()
        if (not user):
            user = self.session.query(User).filter_by(email=login).first()
            if (not user):
                raise UserNotFoundError
        if (not check_password_hash(user.password, password)):
            raise PassNotCorrectError
        token = jwt.encode({"user_id": user.id}, PRIVATE_KEY, algorithm="HS256")
        flask_login.login_user(user)
        return token
        
    def logout(self):
        flask_login.logout_user()
        return ''