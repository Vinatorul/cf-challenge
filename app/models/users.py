from flask_login import UserMixin
from app import *

class Users(db.Model, UserMixin):
    __tablename__= 'users'
    id           = db.Column(db.Integer, primary_key = True, autoincrement = True)
    login        = db.Column(db.String(1000), unique = True, nullable = False)
    role         = db.Column(db.String(50))
    name         = db.Column(db.String(1000))
    handleCFORCE = db.Column(db.String(24)) # Max length of Codeforce's handle = 24 
    handleTIMUS  = db.Column(db.String(50))
    handleINFORM = db.Column(db.String(50))
    password     = db.Column(db.String(1000), nullable = False)
    status       = db.Column(db.String(200))
    vk_url       = db.Column(db.String(100))
    about        = db.Column(db.String(500))

    def __init__(self, login, password, role):
        self.login        = login
        self.password     = password
        self.role         = role
        self.name         = ''
        self.handleCFORCE = ''
        self.handleTIMUS  = ''
        self.handleINFORM = ''
        self.status       = ''
        self.vk_url       = ''
        self.about        = ''

    def set_password(self, password):
        self.password = password
        
    def set_role(self, role):
        self.role = role

    def set_params(self, kwargs):
        self.name         = kwargs['name']
        self.handleCFORCE = kwargs['handleCFORCE']
        self.handleTIMUS  = kwargs['handleTIMUS']
        self.handleINFORM = kwargs['handleINFORM']
        self.status       = kwargs['status']
        self.vk_url       = kwargs['vk_url']
        self.about        = kwargs['about']
