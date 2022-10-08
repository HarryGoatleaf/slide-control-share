from flask import Flask, redirect, url_for
from flask_socketio import SocketIO
from flask_cors import CORS
import os

socketio = SocketIO()

def create_app():
  app = Flask(__name__)

  # load config from environment variables
  # these are defined in docker-compose.yml
  app.config.from_prefixed_env()

  # extensions
  # socketio
  socketio.init_app(app)

  
  # register database stuff
  from . import db
  db.init_app(app)
  
  # register blueprints
  from . import presentation
  app.register_blueprint(user.bp)
  app.register_blueprint(presentation.bp)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # enable cors
  CORS(app, origins=['http://127.0.0.1:*'], supports_credentials=True)

  return app
  
from . import events, user
