from concurrent.futures import thread
from flask import Flask, jsonify, render_template, request, make_response
import time
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading


app = Flask(__name__)


@app.route('/index', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():

  token = request.cookies.get('token')
  
  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)
    currentSession.refreshSession()
    print('token is valid')

    resp = make_response(render_template('index.html', login=True))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
  # Get token from response
  token = request.cookies.get('token')

  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)
    # Since the user has a valid token, redirect them to the challenges page
    resp = make_response(render_template('redirect.html', login=True, redirect_location = "challenge"))
    resp.set_cookie('token', currentSession.token)
    return resp


  if request.method == "POST":
    if request.form['uname'] == "loginCancel":
      resp = make_response(render_template('redirect.html', login=True, redirect_location = 'home'))
      resp.set_cookie('token', '')
      return resp
    
    username = request.form['uname']
    password = request.form['psw']

    # Check if account information is correct
    if accountManager.checkAccount(username, password) == False:
      return "Stupid"
      return render_template('wrongLogin.html')
      
    # Create a new session with the username
    currentSession = sessions(username)
    userSessions.append(currentSession)
    
    #resp = make_response(render_template('challenge.html', login=True))
    resp = make_response(render_template('redirect.html', login=True, redirect_location = 'challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template('login.html', login=True)

@app.route('/register', methods=["POST", "GET"])
def register():
  if request.method == "POST":
    username = request.form['uname']
    password = request.form['psw']

    accountManager.addAccount(username, password)
    
    # Create a new session with the username
    currentSession = sessions(username)
    userSessions.append(currentSession)
    
    #resp = make_response(render_template('challenge.html', login=True))
    resp = make_response(render_template('redirect.html', login=True, redirect_location = 'challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp
  return render_template('login.html')


@app.route('/admin', methods=["POST", "GET"])
def admin():

  token = request.cookies.get('token')

  

  if isSession(token) == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location = "login"))
    resp.set_cookie('token', '')
    return resp
  
  session = getSession(token)
  if accountManager.isAdmin(session.username) == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location = "admin"))
    resp.set_cookie('token', session.token)
    return "You are not an admin"

    resp = make_response(render_template('admin.html', login=True))
    resp.set_cookie('token', session.token)
    return resp

  if request.method == "POST":
    if (request.form['shutdown'] == 'True'):
      accountManager.saveAccounts()

  resp = make_response(render_template('admin.html', login=True))
  resp.set_cookie('token', session.token)
  return resp
  
@app.route('/challenges', methods=["POST", "GET"])
@app.route('/challenge', methods=["POST", "GET"])
def challenge():

  token = request.cookies.get('token')
  if isSession(token) == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location = "login"))
    resp.set_cookie('token', '')
    return resp

  return render_template('challenge.html', login=True)


@app.route('/logout', methods=["POST", "GET"])
def logout():
  token = request.cookies.get('token')
  currentSession = getSession(token)
  currentSession.removeSession()

  resp = make_response(render_template('redirect.html', login=True, redirect_location = "login"))
  resp.set_cookie('token', '')
  return resp 


accountManager.getAccounts()

#print(accountManager.accounts)

threading.Thread(target=removeInactiveSessions).start()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)
