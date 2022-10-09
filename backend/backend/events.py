from . import socketio
from flask_socketio import join_room, leave_room, emit
from flask import current_app, session
from bson.objectid import ObjectId

@socketio.event
def add_me_to_room():
  presentation_id = session.get('presentation_id')
  if presentation_id != None:
    current_app.logger.info('added user to room «%s»', presentation_id)
    join_room(presentation_id)
  else:
    current_app.logger.info('cant add user to room. cookie is «%s»', str(session))