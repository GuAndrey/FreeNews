from datetime import datetime
from sqlalchemy import DATETIME, DateTime, func
from sqlalchemy.orm import Session
from db.connection import ENGINE
from errors.ContentErrors import NoContentError
from models import Favorite, News, User
from module.news.mapper import newsToDto
from errors.AuthErrors import AuthenticationError
from module.news.vo import CATEGORYS, REGIONS
from module.user.commands import UserCommand
import os


class NewsCommand:
    
    def __init__(self):
        self.session = Session(bind=ENGINE)
        self.userCommand = UserCommand()

    def __del__(self):
        self.session.close()

    def getOneNews(self, news_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        news: News = self.session.query(News).filter_by(id=news_id).first()
        if (not news):
            raise NoContentError
        if news.author_id != currentUserId and not news.approved:
            raise AuthenticationError
        return newsToDto(news, currentUserId)
        
    def getNewsList(self, body, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        user: User = self.session.query(User).filter_by(id=currentUserId).first()
        filters = {'approved': True}
        category = body.get('category')
        region = body.get('region')
        sortBy = body.get('sortBy')
        endDate = body.get('endDate')
        startDate = body.get('startDate')
        search = body.get('search')
        onlyFavotite = body.get('onlyFavotite')
        onlySubs = body.get('onlySubs')

        if REGIONS.count(region) > 0: 
            filters['region'] = region
        if CATEGORYS.count(category) > 0: 
            filters['category'] = category
        query = self.session.query(News).filter_by(**filters)
        
        if onlySubs and user:
            query = query.filter(News.author_id.in_(list(map(lambda sub: sub.id_sub, user.subscribe))) )
        if onlyFavotite and user:
            favorite = self.session.query(Favorite).filter_by(id_user=user.id)
            query = query.filter( News.id.in_( list(map(lambda fav: fav.id_news, favorite)) ) )
            
        if startDate and startDate != '':
            query = query.filter(News.create_at >= startDate)
        if endDate and endDate != '':
            endDate += ' 23:59:59'
            query = query.filter(News.create_at <= endDate)
            
        if sortBy == 'Дате (сначала новые)' :
            query = query.order_by(News.create_at.desc())
        elif sortBy == 'Дате (сначала старые)' :
            query = query.order_by(News.create_at)
        elif sortBy == 'Популярности (убыв.)' :
            query = query.order_by(News.total_likes.desc())
        elif sortBy == 'Популярности (возр.)' :
            query = query.order_by(News.total_likes)
        elif sortBy == 'Достоверности (убыв.)' :
            query = query.order_by(News.total_reputations.desc())
        elif sortBy == 'Достоверности (возр.)' :
            query = query.order_by(News.total_reputations)
        elif sortBy == 'Просмотрам (убыв.)' :
            query = query.order_by(News.total_views.desc())
        elif sortBy == 'Просмотрам (возр.)' :
            query = query.order_by(News.total_views)
            
        if search and search != '':
            query = query.filter(News.title_lower.ilike(f'%{search}%'))
            
        newsList = query.all()
        if (newsList):
            return list(map(lambda news: newsToDto(news, currentUserId), newsList))
        else:
            notFoundNews = self.session.query(News).filter_by(id=0).first()
            return [newsToDto(notFoundNews, currentUserId)]
            
    def getNewsListByAuthor(self, author_id, cookies):
        currentUserId = self.userCommand.getCurrentUserId(cookies)
        if currentUserId == author_id:
            newsList = self.session.query(News).filter_by(author_id=author_id).order_by(News.create_at.desc()).all()
        else:
            newsList = self.session.query(News).filter_by(approved=True, author_id=author_id).order_by(News.create_at.desc()).all()
        if (newsList):
            return list(map(lambda news: newsToDto(news, currentUserId), newsList))
        else:
            return []
            
    def addNews(self, title, content, region, category, cookies):
        user_id = self.userCommand.getCurrentUserId(cookies)
        if user_id == -1:
            raise AuthenticationError
        if REGIONS.count(region) == 0: region = '-'
        if CATEGORYS.count(category) == 0: category = 'Другое'
        news = News()
        news.title = title
        news.title_lower = title.lower()
        news.author_id = user_id
        news.content = content
        news.region = region
        news.category = category
        news.create_at = datetime.now()
        news.update_at = datetime.now()
        news.resource = "assets/images/preview.png"
        self.session.add(news)
        self.session.commit()
        return newsToDto(news, user_id)
        
    def addNewsResourse(self, resourse, news_id, cookies):
        user_id = self.userCommand.getCurrentUserId(cookies)
        news: News = self.session.query(News).filter_by(id=news_id).first()
        if not news:
            raise NoContentError
        if user_id == -1 or user_id != news.author_id:
            raise AuthenticationError
        filename = 'newResourse' + str(news_id) + '.png'
        file_path = 'news_resource_storage/' + filename
        if os.path.exists(file_path):
            os.remove(file_path)
        resourse.save(file_path)
        
    def deleteNews(self, news_id, cookies):
        user_id = self.userCommand.getCurrentUserId(cookies)
        news: News = self.session.query(News).filter_by(id=news_id).first()
        if not news:
            raise NoContentError
        if user_id == -1 or user_id != news.author_id:
            raise AuthenticationError
        filename = 'newResourse' + str(news_id) + '.png'
        file_path = 'news_resource_storage/' + filename
        if os.path.exists(file_path):
            os.remove(file_path)
        self.session.delete(news)
        self.session.commit()
        