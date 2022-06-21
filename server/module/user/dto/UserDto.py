from datetime import datetime

class UserDto:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.login = ''
        self.password = ''
        self.birthday = ''
        self.reg_date = ''
        self.description = ''
        self.role = ''
        self.subs = 0
        self.to_subs = 0
        self.materials = []
        self.avatar = ''
        self.current = False
        self.sub_by_current = False
        self.total_rep = 0
        self.total_likes = 0
        self.total_views = 0
        self.total_news = 0

