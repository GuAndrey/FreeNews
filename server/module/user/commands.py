import os
from sqlalchemy.orm import Session
from db.connection import ENGINE
from errors.AuthErrors import AuthenticationError
from models import User
from module.user.mapper import userToDto
import jwt
from config.globals import PRIVATE_KEY


class UserCommand:
    def __init__(self):
        self.session = Session(bind=ENGINE)

    def __del__(self):
        self.session.close()
        
    def getCurrentUserId(self, cookies):
        try:
            current_id = jwt.decode(cookies['new_session'], PRIVATE_KEY, algorithms=['HS256'])['user_id']
        except Exception:
            current_id = -1
        return current_id 
        
    def getOneUser(self, user_id, cookies):
        user = self.session.query(User).filter_by(id=user_id).first()
        if (user):
            currentUserId = self.getCurrentUserId(cookies)
            return userToDto(user, currentUserId)
        else:
            return {}
            
    def getUserList(self, body, cookies):
        currentUserId = self.getCurrentUserId(cookies)
        user: User = self.session.query(User).filter_by(id=currentUserId).first()
        search = body.get('search')
        sortBy = body.get('sortBy')
        sortByField = body.get('sortByField')
        onlySubs = body.get('onlySubs')

        query = self.session.query(User).filter_by(role = 1)

        if onlySubs and currentUserId != -1:
            query = query.filter(User.id.in_(list(map(lambda sub: sub.id_sub, user.subscribe))) )
            
        queryLogin = None
        queryName = None
        if search and search != '':
            queryLogin = query.filter(User.login.ilike(f'%{search}%'))
            queryName = query.filter(User.name.ilike(f'%{search}%'))
        if queryLogin or queryName:
            userList = queryName.all()
            userList.extend(queryLogin.all())
            userList = list(set(userList))
        else:
            userList = query.all()
            
        if sortBy == 'Возрастанию':
            reverse = False
        else:
            reverse = True
        if sortByField == 'Подписчикам':
            userList = sorted(userList, key=lambda x: x.total_subscribers, reverse=reverse )
        elif sortByField == 'Популярности':
            userList = sorted(userList, key=lambda x: x.total_likes, reverse=reverse )
        elif sortByField == 'Доверию':
            userList = sorted(userList, key=lambda x: x.total_rep, reverse=reverse )
        elif sortByField == 'Просмотрам':
            userList = sorted(userList, key=lambda x: x.total_views, reverse=reverse )
        elif sortByField == 'Кол-во новостей':
            userList = sorted(userList, key=lambda x: x.total_news, reverse=reverse )
        elif sortByField == 'Алфавиту':
            userList = sorted(userList, key=lambda x: x.name, reverse=reverse )
            
        if (userList):            
            return list(map(lambda x: userToDto(x, currentUserId), userList))
        else:
            notFoundUsers = self.session.query(User).filter_by(id=0).first()
            return [userToDto(notFoundUsers, currentUserId)]
            
    def addUserAvatar(self, resourse, cookies):
        user_id = self.getCurrentUserId(cookies)
        if user_id == -1:
            raise AuthenticationError
        filename = 'userAvatar' + str(user_id) + '.png'
        file_path = 'users_avatar_storage/' + filename
        if os.path.exists(file_path):
            os.remove(file_path)
        resourse.save(file_path)
        
    def swapRole(self, cookies):
        user_id = self.getCurrentUserId(cookies)
        if user_id == -1:
            raise AuthenticationError
        user: User = self.session.query(User).filter_by(id=user_id).first()
        if user.role == 1:
            user.role = 0
        elif user.role == 0:
            user.role = 1
        self.session.commit()
        return userToDto(user, user_id)
        
    def editUser(self, user_id, description, cookies):
        curr_user_id = self.getCurrentUserId(cookies)
        user: User = self.session.query(User).filter_by(id=user_id).first()
        if curr_user_id == -1 or not user or user_id != curr_user_id:
            raise AuthenticationError
        if description:
            user.description = description
        self.session.commit()
        return userToDto(user, user_id)
        