from flask import Flask, render_template, redirect, url_for, session, request, current_app, g
from flask_socketio import SocketIO
import flask_sijax
import os
import json
from bson.objectid import ObjectId

def create_app():
  app = Flask(__name__)

  # load config from environment variables
  # these are defined in docker-compose.yml
  app.config.from_prefixed_env()

  # extensions
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

  @app.route('/')
  def landing_page():
    return redirect(url_for('presentation.create'))

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass


  return app

def init_socketio(app):
  # socketio
  socketio = SocketIO(app)
    
  @socketio.event
  def set_slide(set_slide_msg):
    new_slide = int(set_slide_msg.get('new_slide'))
    if new_slide == None:
      current_app.logger.error("set_slide: malformed request")
      return

    # check if user is in presentation
    presentation_id = session.get('presentation_id')
    if presentation_id == None:
      current_app.logger.error("socket accessed nonexistent presentation")
      return

    # load database
    from . import db
    db = db.get_db()
    presentations = db['presentations']
    # change current slide in db
    presentations.update_one({"_id": ObjectId(presentation_id)}, {'$set': {'current_slide': new_slide}})
    
    # broadcast new slide to all clients

  return app, socketio