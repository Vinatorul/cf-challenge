from secret import secret_key
from app import app, db
from views import index, users, contests, login, profile, register, logout, settings, images, p404, edit


if __name__ == "__main__":
	app.secret_key = secret_key
	app.run(debug=True)
