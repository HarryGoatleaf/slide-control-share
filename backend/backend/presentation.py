from flask import Blueprint, g, redirect, render_template, url_for, session, request, current_app, abort, send_file
from .db import Presentation,User
from .user import name_required
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from . import socketio
from flask_socketio import leave_room
import os
from PyPDF2 import PdfReader
import io

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
  if not 'slides' in request.files:
    return {'status': 'failed', 'message': 'missing slides'}
  if not allowed_file(request.files['slides'].filename):
    return {'status': 'failed', 'message': 'only pdfs allowed'}
  # read the pdf into memory so we can read it multiple times
  # otherwise the buffer is empty after creating PdfReader
  # TODO: maybe there is a better way to do this
  file = request.files['slides'].read()
  try:
    pdf = PdfReader(io.BytesIO(file))
  except Exception as e:
    return {'status': 'failed', 'message': 'corrupt pdf'}

  # create database object of presentation
  presentation = Presentation(
    host = g.user,
    users = [g.user],
    current_slide = 1,
    num_slides = len(pdf.pages),
    )
  # save slides in DB
  presentation.slides.put(file, content_type = 'application/pdf')
  presentation.save()

  # set users current presentation id to the one created
  presentation_id = str(presentation.id)
  session['presentation_id'] = presentation_id

  # log
  current_app.logger.info('User «%s» created presentation «%s» ',
    g.user.encode(),
    presentation.encode())

  return {'status': 'success', 'presentation': presentation.encode()}

@bp.route('/<string:presentation_id>')
@name_required
def presentation(presentation_id):
  # case: user joins presentation
  if g.presentation == None:
    return join_presentation(presentation_id)

  # case: user reloads page
  elif str(g.presentation.id) == presentation_id:
    return { 'status': 'success', 'presentation': g.presentation.encode() }

  # case: user is already in another session
  else:
    # TODO: what to do if user is already in another session?
    #       currently: join new session
    current_app.logger.info("Moving user from presentation «%s» to «%s»",
      str(g.presentation.id),
      presentation_id)
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
    msg = request.get_json()
    new_slide = msg.get('new_slide')
    if new_slide==None:
      return {'status': 'failed', 'message': 'malformed'}
    if new_slide < 1 or g.presentation.num_slides < new_slide:
      return {'status': 'failed', 'message': 'malformed'}

    # change current slide in db
    g.presentation.current_slide = new_slide
    g.presentation.save()
    # broadcast new slide to all clients in presentation group
    socketio.emit('set_slide', new_slide, to=presentation_id)

    # log
    current_app.logger.info("Set slide to %s", new_slide)
    return {'status': 'success'}

@bp.route('/<string:presentation_id>/slides', methods =['GET'])
@name_required
def slides(presentation_id):
  # TODO: is this nice?
  if g.presentation == None:
    return {'status': 'failed', 'message': 'not in a presentation'}
  if not str(g.presentation.id) == presentation_id:
    return {'status': 'failed', 'message': 'wrong presentation'}

  if request.method == 'GET':
    return send_file(g.presentation.slides, as_attachment=True, mimetype='application/pdf', download_name='slides.pdf')


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
  if not g.user in g.presentation.users: # this might be superfluous
    # add user to presentation in database
    g.presentation.users.append(g.user)
    g.presentation.save()
    # TODO: REFACTOR THIS. currently sending whole presentation
    # becuase of lack of proper encoding
    socketio.emit('set_users',
     g.presentation.encode(),
     to=presentation_id)

    # log
    current_app.logger.info('Added user «%s» to session «%s»',
      str(g.user.name),
      str(g.presentation.id))

  return { 'status': 'success', 'presentation': g.presentation.encode() }

def leave_current_presentation():
  """ Leaves the presentation saved in the session cookie """
  if g.presentation == None:
    return

  # remove user from db presentation object
  g.presentation.update(pull__users=g.user)
  g.presentation.save()

  # leave presentation broadcast room
  # TODO: should we loave the broadcast room here?
  # NOTE: broadcast rooms are automatically left on disconnect.
  #       because the client connection gets started in Presentation.vue
  #       the room should automatically be left when changing presentations.
  # leave_room(str(g.presentation.id))
  # TODO: broadcast leave to other users

  # remove presentation from session
  session['presentation_id'] = None

  current_app.logger.info('Removed user «%s» from session «%s»',
    str(g.user.id),
    str(g.presentation.id))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS