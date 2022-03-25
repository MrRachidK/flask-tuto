import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from channel_app import views
from channel_app import model

@login_manager.user_loader
def load_user(user_id):
    return model.User.query.get(int(user_id))

@app.cli.command("init_db")
def init_db():
    model.init_db()

