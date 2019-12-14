from secret import secret_key
from app import app, db
from views import view, users, contests, login, profile, register, logout, settings, images


if __name__ == "__main__":
	app.secret_key = secret_key #str(), it's necessary..
	app.run(debug=True)
