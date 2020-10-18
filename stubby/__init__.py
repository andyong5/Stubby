from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
moment = Moment(app)
from stubby import routes
