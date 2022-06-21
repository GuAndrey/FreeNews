import base64
import os
from models import News
from module.news.dto.NewsDto import NewsDto
from models import Comment
from module.comment.dto.CommentDto import CommentDto


def commentToDto(comment: Comment, currentUserId: int):
    commentDto = CommentDto()
    commentDto.id = comment.id
    commentDto.id_news = comment.id_news
    commentDto.content = comment.content
    commentDto.publish_date = comment.create_at.date().strftime("%d %B %Y")
    commentDto.author_name = comment.user.name
    commentDto.author_avatar = comment.user.avatar
    res_path = f'users_avatar_storage/userAvatar{comment.user.id}.png'

    if os.path.exists(res_path):
        with open(res_path, "rb") as res:
            thumb_string = str(base64.b64encode(res.read()))
        commentDto.author_avatar  = "data:image/jpeg;base64," + str(thumb_string)[2:-1]
    else:
        commentDto.author_avatar = comment.user.avatar

    commentDto.by_current = comment.id_user == currentUserId

    return commentDto