from pymongo import MongoClient

from flask import current_app, g

def get_db():
    if 'db' not in g:
        client = MongoClient(
            current_app.config['DATABASE']
        )
        g.db = client['slide-control-share']
        g.db_client = client
    return g.db

# what does e=none do??
# copied from tutorial
def close_db(e=None):
    db_client = g.pop('db_client', None)

    if db_client is not None:
        g.pop('db', None)
        # hopefully this is correct for MongoDB ... at least the method exists ...
        db_client.close()
        
# register new methods with flask
def init_app(app):
    # this tells flask that it needs to call close_db when stopping app
    app.teardown_appcontext(close_db)