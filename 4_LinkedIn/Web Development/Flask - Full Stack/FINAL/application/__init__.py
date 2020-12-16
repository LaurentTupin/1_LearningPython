from flask import Flask
from flask_restplus import Api
from config import Config
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(Config)
api = Api()

db = MongoEngine()
db.init_app(app)
api.init_app(app)

# List Of Area

# Dico Area: [PCF]

from application import routes
