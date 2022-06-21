from sqlalchemy.orm import Session
from db.connection import ENGINE
from module.user.mapper import userToDto
from module.user.commands import UserCommand
from errors.AuthErrors import AuthenticationError
from models import Like, News, Subscribe
from models import Reputation
from models import View
from models import Favorite


class StatCommand:
    def __init__(self):
        self.session = Session(bind=ENGINE)
        self.userCommand = UserCommand()

    def __del__(self):
        self.session.close()
        
    def swapLike(self, news_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == -1:
            raise AuthenticationError
        like = self.session.query(Like).filter_by(id_user=currentUserId, id_news=news_id).first()
        if like:
            self.session.delete(like)
        else:
            newLike = Like()
            newLike.id_news = news_id
            newLike.id_user = currentUserId
            self.session.add(newLike)
        self.session.commit()
        
    def swapSubscribe(self, sub_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == -1:
            raise AuthenticationError
        sub = self.session.query(Subscribe).filter_by(id_user=currentUserId, id_sub=sub_id).first()
        if sub:
            self.session.delete(sub)
        else:
            newSub = Subscribe()
            newSub.id_sub = sub_id
            newSub.id_user = currentUserId
            self.session.add(newSub)
        self.session.commit()
        
    def swapRep(self, news_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == -1:
            raise AuthenticationError
        rep = self.session.query(Reputation).filter_by(id_user=currentUserId, id_news=news_id).first()
        if rep:
            self.session.delete(rep)
        else:
            newRep = Reputation()
            newRep.id_news = news_id
            newRep.id_user = currentUserId
            self.session.add(newRep)
        self.session.commit()
        
    def swapFavorite(self, news_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == -1:
            raise AuthenticationError
        favorite = self.session.query(Favorite).filter_by(id_user=currentUserId, id_news=news_id).first()
        if favorite:
            self.session.delete(favorite)
        else:
            newFavorite = Favorite()
            newFavorite.id_news = news_id
            newFavorite.id_user = currentUserId
            self.session.add(newFavorite)
        self.session.commit()
        
    def addView(self, news_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == -1:
            raise AuthenticationError
        view = self.session.query(View).filter_by(id_user=currentUserId, id_news=news_id).first()
        if not view:
            newView = View()
            newView.id_news = news_id
            newView.id_user = currentUserId
            self.session.add(newView)
        self.session.commit()

        