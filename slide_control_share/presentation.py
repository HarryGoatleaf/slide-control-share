from flask import Blueprint, g, redirect, render_template, url_for, session, request, current_app, abort
from slide_control_share.db import get_db
from slide_control_share.hello import name_required
from bson.objectid import ObjectId
from . import socketio

bp = Blueprint('presentation', __name__, url_prefix="/presentation")

@bp.route('/create', methods = ['GET', 'POST'])
@name_required
def create():
  if request.method == 'GET':
    return render_template('create.html')
  elif request.method == 'POST':
    # load database
    db = get_db()
    presentations = db['presentations']

    # create presentation object
    presentation = { 
      "host": g.user['_id'],
      "users": [g.user['_id']],
      "content": request.form['content'],
      "current_slide": 0
      }
    # insert presentation in database
    presentation_id = str(presentations.insert_one(presentation).inserted_id)
    # set users current presentation to the one created
    session['presentation_id'] = presentation_id

    # log
    current_app.logger.info('User «%s» created presentation «%s» ', 
      g.user['name'], 
      presentation_id)

    return redirect(url_for('presentation.presentation', presentation_id = presentation_id))

@bp.route('/<string:presentation_id>')
@name_required
def presentation(presentation_id):
  if g.presentation == None: # case: user joins presentation
    # get presentations from db
    presentations = get_db()['presentations']
    # fetch requested presentation from database
    req_pres = presentations.find_one({"_id": ObjectId(presentation_id)})
    # check if requested presentation exists
    if req_pres == None:
      abort(404)

    # join presentation client side
    session['presentation_id'] = presentation_id
    load_presentation()
    # join presentation on server side
    if not g.user['_id'] in g.presentation['users']: # this might be superfluous
      # add user to presentation in database
      presentations.update_one({"_id": g.presentation['_id']}, {'$push': {'users': g.user['_id']}})
      # update local data. database query might be unnecesary
      g.presentation = presentations.find_one({"_id": ObjectId(presentation_id)})
      # TODO: broadcast new user to other users
      # log
      current_app.logger.info('Added user «%s» to session «%s»', 
        str(g.user['_id']),
        str(g.presentation['_id']))
  elif str(g.presentation['_id']) == presentation_id: # case: user reloads page
    pass
  else:
    # TODO: what to do if user is already in another session?
    #       currently: redirect to current session
    current_app.logger.info("switching presentations?")
    redirect(url_for('presentation.presentation', presentation_id = str(g.presentation['_id'])))
  return render_template('presentation.html', user = g.user, presentation = g.presentation)

@bp.before_request
def load_presentation():
  presentation_id = session.get('presentation_id')

  if presentation_id is None:
    g.presentation = None
  else:
    presentations = get_db()['presentations']
    g.presentation = presentations.find_one({"_id": ObjectId(presentation_id)})
    # TODO: user_id's cant be forged but can it happen that they do not exist in db?