from app import db, Users, Contests

db.drop_all()
db.create_all()

#Just for recreate databases, tests
new_user = Users("handle", "name")
db.session.add(new_user)

new_contest = Contests(123, "awd")
db.session.add(new_contest)

db.session.commit()