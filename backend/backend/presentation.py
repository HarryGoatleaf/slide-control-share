from flask import Blueprint, g, redirect, render_template, url_for, session, request, current_app, abort
from .db import Presentation,User
from .user import name_required
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from . import socketio
from flask_socketio import leave_room

bp = Blueprint('presentation', __name__, url_prefix="/api/presentation")

from flask_cors import CORS
CORS(bp, origins=['http://127.0.0.1:*'], supports_credentials=True)

@bp.before_request
def load_presentation():
  """ Loads the presentation data from the database into the request-scope 'g' object. """
  presentation_id = session.get('presentation_id')

  if presentation_id is None:
    g.presentation = None
  else:
    g.presentation = Presentation.objects.get(id=ObjectId(presentation_id))
    # TODO: presentation_id's cant be forged but can it happen that they do not exist in db?

# routes
@bp.route('/create', methods = ['POST'])
@name_required
def create():
  # verify request
  new_presentation = request.get_json()
  if not 'content' in new_presentation:
    return {'status': 'failed', 'message': 'malformed'}

  # crate database object of presentation
  presentation = Presentation(
    host = g.user,
    users = [g.user],
    content = new_presentation['content'],
    current_slide = 0,
    ).save()
  # set users current presentation to the one created
  presentation_id = str(presentation.id)
  session['presentation_id'] = presentation_id

  # log
  current_app.logger.info('User «%s» created presentation «%s» ', 
    g.user['name'], 
    presentation_id)

  return {'status': 'success', 'presentation': presentation.to_json()}

@bp.route('/<string:presentation_id>')
@name_required
def presentation(presentation_id):
  # case: user joins presentation
  if g.presentation == None: 
    return join_presentation(presentation_id)

  # case: user reloads page
  elif str(g.presentation.id) == presentation_id: 
    return { 'status': 'success', 'presentation': g.presentation.to_json() }

  # case: user is already in another session
  else:
    # TODO: what to do if user is already in another session?
    #       currently: join new session
    leave_current_presentation()
    return join_presentation(presentation_id)

@bp.route('/<string:presentation_id>/current_slide', methods =['GET', 'POST'])
@name_required
def current_slide(presentation_id):
  # TODO: is this nice?
  if g.presentation == None:
    return {'status': 'failed', 'message': 'not in a presentation'}
  if not str(g.presentation.id) == presentation_id:
    return {'status': 'failed', 'message': 'wrong presentation'}

  if request.method == 'GET':
    # TODO: is the GET route neccesary?
    return {'status': 'success', 'current_slide': g.presentation.current_slide}

  elif request.method == 'POST':
    # verify request
    new_slide = request.get_json()
    if not 'new_slide' in new_slide:
      return {'status': 'failed', 'message': 'malformed'}

    # change current slide in db
    g.presentation.current_slide = new_slide['new_slide']
    g.presentation.save()
    # broadcast new slide to all clients in presentation group
    socketio.emit('set_slide', new_slide['new_slide'], to=presentation_id)

    # log
    current_app.logger.info("Set slide to %s", new_slide['new_slide'])
    return {'status': 'success'}

# helper methods
def join_presentation(presentation_id):
  """ Tries to join <presentation_id> and returns API response JSON """
  # fetch requested presentation from database
  try:
    presentation = Presentation.objects.get(id=ObjectId(presentation_id))
  except:
    return {'status': 'failed', 'message': 'presentation does not exist'}

  # add presentation to user session data
  session['presentation_id'] = presentation_id
  load_presentation()
  # add user to presentation in database
  if not g.user.id in g.presentation.users: # this might be superfluous
    # add user to presentation in database
    g.presentation.users.append(g.user.id)
    g.presentation.save()
    # TODO: REFACTOR THIS. currently sending whole presentation 
    # becuase of lack of proper encoding
    socketio.emit('set_users',
     g.presentation.to_json(),
     to=presentation_id)

    # log
    current_app.logger.info('Added user «%s» to session «%s»', 
      str(g.user.name),
      str(g.presentation.id))

  return { 'status': 'success', 'presentation': g.presentation.to_json() }
    
def leave_current_presentation():
  """ Leaves the presentation saved in the session cookie """
  if g.presentation == None:
    return

  # remove user from db
  g.presentation.users.remove(g.user.id)
  g.presentation.save()
  # remove presentation from session
  session['presentation_id'] = None
  
  # TODO: broadcast leave to other users
  # leave presentation broadcast room
  # TODO: should we loave the broadcast room here?
  # leave_room(presentation_id)

  current_app.logger.info('Removed user «%s» from session «%s»',
    str(g.user.id),
    str(presentation.id))
