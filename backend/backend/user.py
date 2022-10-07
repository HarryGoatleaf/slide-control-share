from flask import Blueprint, g, redirect, session, request, current_app
from .db import get_db
from bson.objectid import ObjectId
import functools

bp = Blueprint('user', __name__, url_prefix='/api/user')

from flask_cors import CORS
CORS(bp, origins=['http://127.0.0.1:*'], supports_credentials=True)

@bp.route('/name', methods = ['GET', 'POST'])
def name():
  if request.method == 'GET':
    if g.user == None:
      return {'status': 'failed', 'message': 'unknown user'}
    else:
      return {'status': 'success', 'user': {'name': g.user['name'], 'id': str(g.user['_id'])}}
  elif request.method == 'POST':
    if g.user == None:

      new_user = request.get_json()
      # validate request
      if not 'username' in new_user:
        return {'status': 'failed', 'message': 'malformed'}

      # load database
      db = get_db()
      users = db['users']
      # create user object
      user = { 'name': new_user['username'] }
      # insert user in database
      user_id = str(users.insert_one(user).inserted_id)

      # load user data into session
      session['user_id'] = user_id
      load_user()

      # log
      current_app.logger.info('Created user «%s»', user['name'])

      return {'status': 'success', 'user': {'name': g.user['name'], 'id': str(g.user['_id'])}}
    else:
      # TODO: what happens if an already registered user sets a new name? 
      #       this currently cant happen
      pass
      
@bp.before_app_request
def load_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db()['users'].find_one({"_id": ObjectId(user_id)}) 
    # TODO: user_id's cant be forged but can it happen that they do not exist in db?

def name_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return {'status': 'failed', 'message': 'unknown user'}
    return view(**kwargs)
  return wrapped_view
