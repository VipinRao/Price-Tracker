from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import redis
from rq import Queue
import rq
app = Flask(__name__)
# app.redis = redis.Redis.from_url('redis://')
# app.task_queue = rq.Queue(connection=app.redis)
app.config['SECRET_KEY'] = '57c71278511bcf1bd5d494ddeffb0dcd' #for security purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #///means relative path, site.db will be file to store database
db = SQLAlchemy(app)  #DATABASE INSTANCE
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  #function name for the route ,so that login manager can redirect unauthorized access to login page
login_manager.login_message_category = 'info' #info is bootstap class for style
from pricetracker import routes
