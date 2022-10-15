from flask import Flask, jsonify, render_template, request, make_response
import time
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading
import subprocess
import yml

app = Flask(__name__)


def refreshSession(token):
  currentSession = getSession(token)
  currentSession.refreshSession()
  return currentSession

def invalidSession(token):
  resp = make_response(render_template('redirect.html', login=True, redirect_location="login"))
  resp.set_cookie('token', '')
  return resp



def runPeriodically():
  accountManager.saveAccounts()
  removeInactiveSessions()


@app.route('/index', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():

  token = request.cookies.get('token')

  if isSession(token) and request.method == "GET" and token != None:

    #print('token is valid')
    currentSession = refreshSession(token)

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
    resp = make_response(
      render_template('redirect.html', login=True, redirect_location="challenge"))
    resp.set_cookie('token', currentSession.token)
    return resp

  if request.method == "POST":
    if request.form['uname'] == "loginCancel":
      resp = make_response(render_template('redirect.html', login=True, redirect_location='home'))
      resp.set_cookie('token', '')
      return resp #hello

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
    resp = make_response(render_template('redirect.html', login=True, redirect_location='challenge'))
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
    resp = make_response(
      render_template('redirect.html', login=True, redirect_location='challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp
  return render_template('login.html')


@app.route('/admin', methods=["POST", "GET"])
def admin():

  token = request.cookies.get('token')

  if isSession(token) == False:
   return invalidSession(token)

  session = getSession(token)
  if accountManager.isAdmin(session.username) == False:
    resp = make_response("You are not an admin")
    resp.set_cookie('token', "")
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
    invalidSession(token)
    
  currentSession = refreshSession(token)
  resp = make_response(render_template('challenge.html', login=True))
  resp.set_cookie('token', currentSession.token)
  return resp


@app.route('/logout', methods=["POST", "GET"])
def logout():
  token = request.cookies.get('token')
  currentSession = getSession(token)
  currentSession.removeSession()

  return invalidSession(token)


@app.route('/saveaccounts', methods=["POST", "GET"])
def saveAccounts():
  accountManager.saveAccounts()
  return "done"


@app.route('/test', methods=["POST", "GET"])
def test():
  #print(yml.data['firstCode']['page'])

  if request.method == "POST":
    return "here"
  
  return render_template("test.html", data=yml.data, page="firstCode")

  
@app.route('/recieve_data', methods=["POST", "GET"])
def recieve_code():
  token = request.args.get('token')
  currentSession = getSession(token)
  if currentSession == None:
    return personalFunctions.base64encode("<p><a href=\"login\">Please log in</a></p>".encode())
  
  code = request.args.get('code')
  program = personalFunctions.base64decode(code).decode('utf-8').replace("'", "\"")
  
  if "subprocess" in program or "import os" in program or "from os" in program:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p>We have detected you are trying to gain access to our systems.\nThis incident has been reported.</p>").encode())
  
  #print(program)
  output = personalFunctions.runCode(program, currentSession.token)  
  return personalFunctions.base64encode(personalFunctions.replaceNewlines(output).encode())


accountManager.getAccounts()

#print(accountManager.accounts)

#threading.Thread(target=removeInactiveSessions).start()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
