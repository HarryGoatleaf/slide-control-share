from . import socketio
from flask_socketio import join_room, leave_room
from flask import current_app, session
from bson.objectid import ObjectId

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
  socketio.emit('set_slide', set_slide_msg, to=presentation_id)

  # log
  current_app.logger.info("Set slide to %s", new_slide)
  
@socketio.event
def add_me_to_room():
  presentation_id = session.get('presentation_id')
  if presentation_id != None:
    current_app.logger.info("added user to room «%s»", presentation_id)
    join_room(presentation_id)