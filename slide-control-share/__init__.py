from flask import Flask, render_template, redirect, url_for, session, request
from pymongo import MongoClient

# instantiating flask object
app=Flask(__name__)
# set secret key
app.secret_key = b'veryverysecretkey'

@app.route('/', methods = ['GET', 'POST'])
def hello():
  if request.method == 'GET':
    return render_template('hello.html')
  else:
    session['username'] = request.form['username']
    return create_session()

# helper method => no route
def create_session():
  # TODO: actually create session
  return redirect(url_for('presentation', presentation_id = 420))

@app.route('/presentation/<int:presentation_id>')
def presentation(presentation_id):
  return render_template('presentation.html', presentation_id = presentation_id)

# start server
# NO CODE BELOW THIS
if __name__=='__main__':
  app.debug=True # setting the debugging option for the application instance
  app.run() # launching the flask's integrated development webserver