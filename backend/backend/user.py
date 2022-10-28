from flask import Blueprint, g, redirect, session, request, current_app
from .db import User
from bson.objectid import ObjectId
import functools

bp = Blueprint('user', __name__, url_prefix='/api/user')

from flask_cors import CORS
CORS(bp, origins=['http://127.0.0.1:*'], supports_credentials=True)

@bp.before_app_request
def load_user():
  """ Loads the user data from the database into the request-scope 'g' object. """
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = User.objects.get(id=ObjectId(user_id))
    # TODO: user_id's in cookies can't be forged but can it happen that they do not exist in db?

def name_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return {'status': 'failed', 'message': 'unknown user'}
    return view(**kwargs)
  return wrapped_view

# routes
@bp.route('/name', methods = ['GET', 'POST'])
def name():
  if request.method == 'GET':
    if g.user == None:
      return {'status': 'failed', 'message': 'unknown user'}
    else:
      return {'status': 'success', 'user': g.user.encode()}

  elif request.method == 'POST':
    if g.user == None:
      new_user = request.get_json()
      # validate request
      if not 'username' in new_user:
        return {'status': 'failed', 'message': 'malformed'}
      # save user in DB
      user = User(name=new_user['username']).save()
      # load user data into session object in cookie
      session['user_id'] = str(user.id)
      load_user()
      # log
      current_app.logger.info('Created user «%s»', user.encode())

      return {'status': 'success', 'user': user.encode()}
    else:
      # TODO: what happens if an already registered user sets a new name? 
      #       this currently cant happen
      return {'status': 'failed', 'message': 'already registered'}