from app import db
from models import contests, users


db.drop_all()
db.create_all()