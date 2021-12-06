from flask_login import UserMixin,AnonymousUserMixin

class User(UserMixin):
    def __init__(self, id): 
        self.id = id 

    @property
    def role(self):
        if (self.id == 'MRLGAnker'):
            return "WRITER"
        else:
            return "READER"

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.role = 'READER'

class TestUser(AnonymousUserMixin):
    def __init__(self):
        self.role = 'WRITER'