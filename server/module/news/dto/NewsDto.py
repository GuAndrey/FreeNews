from datetime import datetime

class NewsDto:
    def __init__(self):
        self.id = 0
        self.title = ''
        self.content = ''
        self.category = ''
        self.publish_date = datetime.now().isoformat(sep=' ')
        self.region = ''
        self.resources = ''
        self.author_name = ''
        self.viewes = 0
        self.likes = 0
        self.rep = 0
        self.liked = False
        self.plus_rep = False
        self.viewed = False
        self.favorited = False
        self.approved = False
        self.by_current = False

