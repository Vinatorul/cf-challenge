from app import db
from models import contests, users
import hashlib


db.drop_all()
db.create_all()

password = hashlib.sha224("admin".encode('utf-8')).hexdigest()
db.session.add(users.Users('admin', password, role = "SuperAdmin"))
db.session.commit()