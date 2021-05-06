from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__, static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app.routes import api, base

app.register_blueprint(base, url_prefix='/')
app.register_blueprint(api, url_prefix='/api/')