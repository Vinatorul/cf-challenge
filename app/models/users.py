from flask_login import UserMixin
from app import *

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    handle = db.Column(db.String(24), unique=True, nullable = False) # Max length of Codeforce's handle = 24 
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    status = db.Column(db.String(200))
    vk_url = db.Column(db.String(100))
    about = db.Column(db.String(500))

    def __init__(self, handle):
        self.handle = handle
        self.name = ''
        self.status = ''
        self.vk_url = ''
        self.about = ''

    def set_password(self, password):
        self.password = password

    def set_params(self, kwargs):
        self.name = kwargs['name']
        self.status = kwargs['status']
        self.vk_url = kwargs['vk_url']
        self.about = kwargs['about']

    def serialize(self):
        return {
            'handle' : self.handle,
            'name'   : self.name,
            'status' : self.status,
            'vk_url' : self.vk_url,
            'about'  : self.about
        }