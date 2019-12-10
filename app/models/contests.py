from app import *

class Contests(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(1000), unique = True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
        }