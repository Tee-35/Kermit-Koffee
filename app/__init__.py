from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Initialise extensions without binding to an app yet
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind extensions to the app
    db.init_app(app)
    jwt.init_app(app)

    return app