from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from admin_panel import DashboardView, NewsModelView
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import News, User
from sqlalchemy.orm import Session
from db.connection import ENGINE
from module.news.routes import NewsCategoryRoute, NewsRegionRoute, NewsResourceRoute, NewsRoute, NewsListRoute
from module.user.routes import UserAvatarRoute, UserRoute, UserListRoute, UserCurretIdRoute, UserSwapRoleRoute
from module.auth.routes import LoginRoute, RegRoute, LogoutRoute
from module.stat.routes import LikeRoute, SubRoute
from module.stat.routes import RepRoute
from module.comment.routes import CommentRoute
from module.stat.routes import ViewRoute
from module.stat.routes import FavoriteRoute
import flask_login as login


app = Flask(__name__)
app.secret_key = 'super secret key'
session = Session(bind=ENGINE)


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return session.query(User).get(user_id)


init_login()

admin = Admin(app, name='FREENEWS', template_mode='bootstrap3', index_view = DashboardView())
admin.add_view(NewsModelView(News, session))

api = Api(app)
CORS(app, supports_credentials=True)

# Маршруты для новостей
api.add_resource(NewsRoute, '/news/<int:news_id>', '/news')
api.add_resource(NewsResourceRoute, '/add-news-resource/<int:news_id>')
api.add_resource(NewsListRoute, '/newsList')
api.add_resource(NewsCategoryRoute, '/categorys')
api.add_resource(NewsRegionRoute, '/regions')

# Маршруты для пользователей
api.add_resource(UserRoute, '/user/<int:user_id>')
api.add_resource(UserListRoute, '/userList')
api.add_resource(UserCurretIdRoute, '/getCurrentUserId')
api.add_resource(UserAvatarRoute, '/add-user-avatar')
api.add_resource(UserSwapRoleRoute, '/user/swap-role')

# Маршруты для авторизации
api.add_resource(RegRoute, '/registration')
api.add_resource(LoginRoute, '/login')
api.add_resource(LogoutRoute, '/logout')

# Маршруты для статистики
api.add_resource(LikeRoute, '/like/<int:news_id>')
api.add_resource(RepRoute, '/reputation/<int:news_id>')
api.add_resource(ViewRoute, '/view/<int:news_id>')
api.add_resource(FavoriteRoute, '/favorite/<int:news_id>')
api.add_resource(SubRoute, '/subscribe/<int:sub_id>')

# Маршруты для комментариев
api.add_resource(CommentRoute, '/comment/<int:id>')

if __name__ == '__main__':
    app.run(port=3001, debug=True, host="192.168.199.159")