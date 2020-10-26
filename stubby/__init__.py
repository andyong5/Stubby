from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from stubby.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from stubby.users.routes import users
    from stubby.posts.routes import posts
    from stubby.main.routes import main
    from stubby.errors.handlers import errors

    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
