from flask import Flask, render_template, redirect, url_for, session, request, current_app, g
from flask_socketio import SocketIO
import flask_sijax
import os

def create_app():
  app = Flask(__name__)

  # load config from environment variables
  # these are defined in docker-compose.yml
  app.config.from_prefixed_env()

  # extensions
  # socketio
  socketio = SocketIO()
  socketio.init_app(app)
  # sijax
  sijax = flask_sijax.Sijax()
  sijax.init_app(app)
  
  # register database stuff
  from . import db
  db.init_app(app)
  
  # register blueprints
  from . import hello, presentation
  app.register_blueprint(hello.bp)
  app.register_blueprint(presentation.bp)

  
  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass


  return app