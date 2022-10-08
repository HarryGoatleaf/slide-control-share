from flask import Blueprint, g, redirect, render_template, url_for, session, request, current_app, abort
from .db import Presentation,User
from .user import name_required
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from . import socketio

bp = Blueprint('presentation', __name__, url_prefix="/api/presentation")

from flask_cors import CORS
CORS(bp, origins=['http://127.0.0.1:*'], supports_credentials=True)

@bp.before_request
def load_presentation():
  presentation_id = session.get('presentation_id')

  if presentation_id is None:
    g.presentation = None
  else:
    presentations = Presentation.objects.get(id=ObjectId(presentation_id))
    # TODO: user_id's cant be forged but can it happen that they do not exist in db?

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
  load_presentation()

  # log
  current_app.logger.info('User «%s» created presentation «%s» ', 
    g.user['name'], 
    presentation_id)

  return {'status': 'success', 'presentation': presentation.to_json()}

@bp.route('/<string:presentation_id>')
@name_required
def presentation(presentation_id):
  if g.presentation == None: # case: user joins presentation
    join_presentation(presentation_id)
  elif str(g.presentation.id) == presentation_id: # case: user reloads page
    pass
  else:
    # TODO: what to do if user is already in another session?
    #       currently: redirect to current session
    current_app.logger.info("user already in session")

  # return render_template('presentation.html', user = g.user, presentation = g.presentation)
  return { 'status': 'success', 'presentation': g.presentation.to_json() }

@bp.route('/<string:presentation_id>/current_slide')
@name_required
def current_slide(presentation_id, methods =['GET', 'POST']):
  if request.method == 'GET':
    if g.presentation == None:
      return {'status': 'failed', 'message': 'not in a presentation'}
    else:
      return {'status': 'success', 'current_slide': g.presentation.current_slide}

  elif request.method == 'POST':
    # verify request
    new_slide = request.get_json()
    if not 'new_slide' in new_slide:
      return {'status': 'failed', 'message': 'malformed'}
    # check if user is in a presentation
    if g.presentation == None:
      return {'status': 'failed', 'message': 'not in a presentation'}

    # change current slide in db
    g.presentation.update_one(set__current_slide=new_slide['new_slide'])
    # broadcast new slide to all clients
    socketio.emit('set_slide', new_slide['new_slide'], to=presentation_id)

    # log
    current_app.logger.info("Set slide to %s", new_slide['new_slide'])
    return {'status': 'success'}

# helper methods
def join_presentation(presentation_id):
  # fetch requested presentation from database
  try:
    presentation = Presentation.objects.get(id=ObjectId(presentation_id))
  except:
    print("error presentation does not exist")

  # add presentation to user session data
  session['presentation_id'] = presentation_id
  load_presentation()
  # add user to presentation in database
  if not g.user['_id'] in g.presentation['users']: # this might be superfluous
    # add user to presentation in database
    presentation.update_one(push__users=g.user.id)
    # update local data. database query might be unnecesary
    g.presentation = Presentation.objects.get(id=ObjectId(presentation_id))
    # TODO: broadcast new user to other users

    # log
    current_app.logger.info('Added user «%s» to session «%s»', 
      str(g.user['_id']),
      str(g.presentation['_id']))
