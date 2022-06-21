from datetime import datetime

class CommentDto:
    def __init__(self):
        self.id = 0
        self.content = ''
        self.id_news = 0
        self.publish_date = datetime.now().isoformat(sep=' ')
        self.author_name = ''
        self.author_avatar = ''
        self.by_current = False
