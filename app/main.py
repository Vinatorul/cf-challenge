from app import app, db
from secret import secret_key
import view


if __name__ == "__main__":
	app.secret_key = secret_key #str(), it's necessary..
	app.run(debug=True)
