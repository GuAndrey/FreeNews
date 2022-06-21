from email.policy import default
from itertools import count
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.connection import ENGINE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select


Base = declarative_base(bind=ENGINE)


class User(Base):

    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    role = Column(Integer, nullable=False)
    rep = Column(Integer, nullable=True)
    avatar = Column(String, nullable=True)
    create_at = Column(DateTime, default=now())
    
    news = relationship("News", cascade="all, delete-orphan", back_populates='author')
    likes = relationship("Like", cascade="all, delete-orphan", back_populates='user')
    views = relationship("View", cascade="all, delete-orphan", back_populates='user')
    reputations = relationship("Reputation", cascade="all, delete-orphan", back_populates='user')
    comments = relationship("Comment", cascade="all, delete-orphan", back_populates='user')
    favorites = relationship("Favorite", cascade="all, delete-orphan", back_populates='user')
    subscribe = relationship("Subscribe", cascade="all, delete-orphan", back_populates='user', foreign_keys='Subscribe.id_user')
    subscribers = relationship("Subscribe", cascade="all, delete-orphan", back_populates='sub', foreign_keys='Subscribe.id_sub')

    @hybrid_property
    def total_rep(self):
        return sum( map(lambda one_news: len(one_news.reputations), list(filter(lambda news: news.approved, self.news))) )

    @hybrid_property
    def total_likes(self):
        return sum( map(lambda one_news: len(one_news.likes), list(filter(lambda news: news.approved, self.news))) )

    @hybrid_property
    def total_views(self):
        return sum( map(lambda one_news: len(one_news.views), list(filter(lambda news: news.approved, self.news))) )

    @hybrid_property
    def total_news(self):
        return len(list(filter(lambda news: news.approved, self.news)))

    @hybrid_property
    def total_subscribe(self):
        return len(self.subscribe)

    @hybrid_property
    def total_subscribers(self):
        return len(self.subscribers)
        
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'id: {self.id}\nlogin: {self.login}\nname: {self.name}\ntotal: {self.total_rep}'


class News(Base):

    __tablename__ = 'news'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    title_lower = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    region = Column(String, nullable=True)
    resource = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    create_at = Column(DateTime, default=now())
    update_at = Column(DateTime, nullable=True)
    approved = Column(Boolean, default=False)
    
    author = relationship("User", back_populates='news')
    likes = relationship("Like", cascade="all, delete-orphan", back_populates='news')
    views = relationship("View", cascade="all, delete-orphan", back_populates='news')
    favorites = relationship("Favorite", cascade="all, delete-orphan", back_populates='news')
    reputations = relationship("Reputation", cascade="all, delete-orphan", back_populates='news')
    comments = relationship("Comment", cascade="all, delete-orphan", back_populates='news')
    
    @hybrid_property
    def total_likes(self):
        return len(self.likes)

    @total_likes.expression
    def total_likes(cls):
        return (select([func.count(Like.id_news)]).where(Like.id_news == cls.id)).scalar_subquery()

    @hybrid_property
    def total_views(self):
        return len(self.views)

    @total_views.expression
    def total_views(cls):
        return (select([func.count(View.id_news)]).where(View.id_news == cls.id)).scalar_subquery()

    @hybrid_property
    def total_reputations(self):
        return len(self.reputations)

    @total_reputations.expression
    def total_reputations(cls):
        return (select([func.count(Reputation.id_news)]).where(Reputation.id_news == cls.id)).scalar_subquery()

    @hybrid_property
    def total_comments(self):
        return len(self.comments)

    @total_comments.expression
    def total_comments(cls):
        return (select([func.count(Comment.id_news)]).where(Comment.id_news == cls.id)).scalar_subquery()

    def __repr__(self):
        return f'id: {self.id}\ntitle: {self.title}\nauthor_id: {self.author_id}'

        
class Comment(Base):

    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    id_news = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='comments')
    news = relationship("News", back_populates='comments')
    

class Subscribe(Base):

    __tablename__ = 'subscribe'
    
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    id_sub = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='subscribe', foreign_keys='Subscribe.id_user')
    sub = relationship("User", back_populates='subscribers', foreign_keys='Subscribe.id_sub')
    

class Like(Base):

    __tablename__ = 'like'
    
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    id_news = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='likes')
    news = relationship("News", back_populates='likes')
    

class View(Base):

    __tablename__ = 'view'
    
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    id_news = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='views')
    news = relationship("News", back_populates='views')
    

class Reputation(Base):

    __tablename__ = 'reputation'
    
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    id_news = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='reputations')
    news = relationship("News", back_populates='reputations')
    

class Favorite(Base):

    __tablename__ = 'favorite'
    
    id_user = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    id_news = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
    create_at = Column(DateTime, default=now())
    
    user = relationship("User", back_populates='favorites')
    news = relationship("News", back_populates='favorites')