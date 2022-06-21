import os
from models import News
from module.news.dto.NewsDto import NewsDto
import base64

def newsToDto(news: News, currentUserId: int):
    getOneNewsDto = NewsDto()
    getOneNewsDto.id = news.id
    getOneNewsDto.title = news.title
    getOneNewsDto.content = news.content
    getOneNewsDto.category = news.category
    getOneNewsDto.publish_date = news.create_at.date().strftime("%d %B %Y")
    getOneNewsDto.region = news.region
    getOneNewsDto.author_name = news.author.name
    getOneNewsDto.approved = news.approved
    getOneNewsDto.likes = news.total_likes
    getOneNewsDto.rep = news.total_reputations
    getOneNewsDto.viewes = news.total_views
    getOneNewsDto.by_current = news.author_id == currentUserId

    for like in news.likes:
        if like.id_user == currentUserId:
            getOneNewsDto.liked = True
            break
    for rep in news.reputations:
        if rep.id_user == currentUserId:
            getOneNewsDto.plus_rep = True
            break
    for view in news.views:
        if view.id_user == currentUserId:
            getOneNewsDto.viewed = True
            break
    for favorite in news.favorites:
        if favorite.id_user == currentUserId:
            getOneNewsDto.favorited = True
            break

    res_path = f'news_resource_storage/newResourse{news.id}.png'
    if os.path.exists(res_path):
        with open(res_path, "rb") as res:
            thumb_string = str(base64.b64encode(res.read()))
        getOneNewsDto.resources  = "data:image/jpeg;base64," + str(thumb_string)[2:-1]
    else:
        getOneNewsDto.resources = news.resource
    return getOneNewsDto