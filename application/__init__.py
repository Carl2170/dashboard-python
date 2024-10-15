from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from application import database
app = Flask(__name__)

from application import routes

#database.init_database()



