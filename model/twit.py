from model.user import User


class Twit:
    def __init__(self, body: str, author: User):  # (like: 1 - лайк, 0 - дизлайк)
        self.body = body
        self.author = author
