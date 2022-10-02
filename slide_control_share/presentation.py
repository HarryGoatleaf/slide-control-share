from flask import Blueprint, g, redirect, render_template, url_for, session, request
from slide_control_share.db import get_db
from slide_control_share.hello import name_required
from bson.objectid import ObjectId
import functools

bp = Blueprint('presentation', __name__, url_prefix="/presentation")

@bp.route('/<int:presentation_id>')
@name_required
def presentation(presentation_id):
  return render_template('presentation.html', user = g.user, presentation_id = presentation_id)


def load_presentation():
  presentation_id = session.get('presentation_id')

  if presentation_id is None:
    g.user = None
  else:
    g.user = get_db()['presentations'].find_one({"_id": ObjectId(presentation_id)})
    # TODO: user_id's cant be forged but can it happen that they do not exist in db?