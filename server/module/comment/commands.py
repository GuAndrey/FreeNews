from datetime import datetime
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from db.connection import ENGINE
from config.globals import PRIVATE_KEY
from models import User
from errors.AuthErrors import PassMathError, PassNotCorrectError, UserNotFoundError, UserExistError
from module.user.mapper import userToDto
from module.user.commands import UserCommand
from models import Comment
from module.comment.mapper import commentToDto
from errors.AuthErrors import AuthenticationError
from sqlalchemy import desc
from errors.ContentErrors import NoContentError


class CommentCommand:
    def __init__(self):
        self.session = Session(bind=ENGINE)
        self.userCommand = UserCommand()

    def __del__(self):
        self.session.close()
        
    def getCommentsListByNewsId(self, newsId: int, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        commentList = self.session.query(Comment).filter_by(id_news=newsId).order_by(desc(Comment.create_at))
        if (commentList):
            return list(map(lambda x: commentToDto(x, currentUserId), commentList))
        else:
            return []
            
    def addComment(self, content: str, news_id: int, cookies):
        user_id = self.userCommand.getCurrentUserId(cookies)
        if user_id == -1:
            raise AuthenticationError
        if content == '':
            raise NoContentError
        comment = Comment()
        comment.content = content
        comment.id_news = news_id
        comment.id_user = user_id
        comment.create_at = datetime.now()
        self.session.add(comment)
        self.session.commit()
        return commentToDto(comment, user_id)
        
    def deleteComment(self, comment_id: int, cookies):
        user_id = self.userCommand.getCurrentUserId(cookies)
        comment: Comment = self.session.query(Comment).filter_by(id=comment_id).first()
        if not comment:
            raise NoContentError
        if user_id == -1 or user_id != comment.id_user:
            raise AuthenticationError
        self.session.delete(comment)
        self.session.commit()
        