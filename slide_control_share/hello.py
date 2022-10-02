from flask import Blueprint, g, redirect, render_template, url_for, session, request
from slide_control_share.db import get_db
from bson.objectid import ObjectId
import functools

bp = Blueprint('hello', __name__)

@bp.route('/', methods = ['GET', 'POST'])
def hello():
  if request.method == 'GET':
    return render_template('hello.html')
  else:
    if not 'user_id' in session:
      # new user
      session['username'] = request.form['username']
      db = get_db()
      users = db['users']
      user_id = str(users.insert_one({
        "name": session['username']
      }).inserted_id)
      session['user_id'] = user_id
    return redirect(url_for('presentation.presentation', presentation_id = 420))

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
      return redirect(url_for('hello.hello'))
    return view(**kwargs)
  return wrapped_view