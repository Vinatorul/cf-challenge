from app import *

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    handle = db.Column(db.String(24), unique=True) # Max length of Codeforce's handle = 24 
    name = db.Column(db.String(1000), unique=True)

    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

    def serialize(self):
        return {
            'handle' : self.handle,
            'name' : self.name
        }