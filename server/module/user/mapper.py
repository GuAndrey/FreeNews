import base64
import os
from models import User
from module.user.dto.UserDto import UserDto


def userToDto(user: User, currentUserId: int):
    userDto = UserDto()
    userDto.id = user.id
    userDto.name = user.name
    userDto.login = user.login
    userDto.password = ""
    userDto.reg_date = user.create_at

    if user.description == None:
        userDto.description = 'Описание отсутствует'
    else:
        userDto.description = user.description.strip()
        if userDto.description == "":
            userDto.description = 'Описание отсутствует'

    userDto.role = user.role
    userDto.subs = user.total_subscribers
    userDto.to_subs = user.total_subscribe
    userDto.materials = list(map(lambda x: x.id, user.news))
    userDto.current = user.id == currentUserId
    userDto.total_rep = user.total_rep
    userDto.total_likes = user.total_likes
    userDto.total_views = user.total_views
    userDto.total_news = user.total_news

    for sub in user.subscribers:
        if sub.id_user == currentUserId:
            userDto.sub_by_current = True
            break
        
    res_path = f'users_avatar_storage/userAvatar{user.id}.png'
    if os.path.exists(res_path):
        with open(res_path, "rb") as res:
            thumb_string = str(base64.b64encode(res.read()))
        userDto.avatar  = "data:image/jpeg;base64," + str(thumb_string)[2:-1]
    else:
        userDto.avatar = user.avatar
    return userDto