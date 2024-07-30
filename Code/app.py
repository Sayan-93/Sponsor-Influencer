from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tables.db'
app.config["SECRET_KEY"] = 'a6^kf@4g'
#db.init_app(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)