from flask import Blueprint, g, redirect, render_template, url_for, session, request, current_app
from slide_control_share.db import get_db
from bson.objectid import ObjectId
import functools

bp = Blueprint('hello', __name__)

@bp.route('/<path:req_path>/hello', methods = ['GET', 'POST'])
def hello(req_path):
  if request.method == 'GET' and not 'user_id' in session:
    return render_template('hello.html')
  elif request.method == 'POST':
    if not 'user_id' in session:
      # load database
      db = get_db()
      users = db['users']
      
      # create user object
      user = { 'name': request.form['username'] }
      # insert user in database
      user_id = str(users.insert_one(user).inserted_id)
      session['user_id'] = user_id

      # log
      current_app.logger.info('Created user «%s»', user['name'])
    else:
      # TODO: what happens if an already registered user sets a new name? 
      #       this currently cant happen
      pass

  # user is now named => redirect him to requested path
  return redirect('/' + req_path)

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
      return redirect(request.path + '/hello')
    return view(**kwargs)
  return wrapped_view