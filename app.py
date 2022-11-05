from flask import Flask, jsonify, render_template, request, make_response
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading
import yml
from time import sleep

app = Flask(__name__)


def invalidSession():
  resp = make_response(render_template('redirect.html', login=True, redirect_location="/login"))
  resp.set_cookie('token', '')
  return resp

def removeOldRuns():
  files = personalFunctions.getFiles('programRuns/')
  for file in files:
    valid = False
    for session in userSessions:
      if session.token == file:
        valid = False
    if not valid:
      personalFunctions.deleteFile("programRuns/" + file + ".py")

def runPeriodically():
  while True:
    accountManager.saveAccounts()
    removeInactiveSessions()
    removeOldRuns()
    #print(personalFunctions.convertTime(personalFunctions.time()))
    sleep(10)


@app.route('/index', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():

  token = request.cookies.get('token')

  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)


    resp = make_response(render_template('index.html', login=True, admin=accountManager.isAdmin(currentSession.username)))
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
      render_template('redirect.html', login=True, redirect_location="/challenge"))
    resp.set_cookie('token', currentSession.token)
    return resp

  if request.method == "POST":
    if request.form['uname'] == "loginCancel":
      resp = make_response(render_template('redirect.html', login=True, redirect_location='/home'))
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
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template('login.html')


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
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp
  return render_template('login.html')


@app.route('/admin', methods=["POST", "GET"])
def admin():
  token = request.cookies.get('token')
  currentSession = getSession(token)

  if currentSession == None:
   return invalidSession()

  if accountManager.isAdmin(currentSession.username) == False:
    resp = make_response("You are not an admin")
    resp.set_cookie('token', "")
    return resp
  if request.method == "POST":
    if (request.form['button'] == 'saveAccounts'):
      accountManager.saveAccounts()
    elif (request.form['button'] == 'reloadChallenges'):
      yml.reloadChallenges()
    elif (request.form['button'] == 'challengeSubmit'):
      yml.writeChallenges(request.form['challengeQuestions'])
      yml.reloadChallenges()
    
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/admin'))
    resp.set_cookie('token', currentSession.token)
    return resp
  resp = make_response(render_template('admin.html', login=True, challenges=yml.rawChallengesData))
  resp.set_cookie('token', currentSession.token)
  return resp

@app.route('/challenge_submit', methods=["POST", "GET"])
def challenge_submit():
  return "you did it!"
  
@app.route('/challenges', methods=["POST", "GET"])
@app.route('/challenge', methods=["POST", "GET"])
def challenge():

  token = request.cookies.get('token')
  if isSession(token) == False:
    return invalidSession()
    
  currentSession = getSession(token)
  resp = make_response(render_template('challenge.html', login=True, admin=accountManager.isAdmin(currentSession.username)))
  resp.set_cookie('token', currentSession.token)
  return resp


@app.route('/logout', methods=["POST", "GET"])
def logout():
  token = request.cookies.get('token')
  currentSession = getSession(token)
  currentSession.removeSession()

  return invalidSession()


@app.route('/saveaccounts', methods=["POST", "GET"])
def saveAccounts():
  accountManager.saveAccounts()
  return "done"


@app.route('/test', methods=["POST", "GET"])
def test():
  token = request.cookies.get('token')
  currentSession = getSession(token)

  if currentSession == None:
    return invalidSession()
    
  if accountManager.isAdmin(currentSession.username) == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenges'))
    resp.set_cookie('token', currentSession.token)
    return resp
  
  return render_template("test.html", data=yml.data)

  
@app.route('/recieve_data', methods=["POST", "GET"])
def recieve_code():
  token = request.args.get('token')
  currentSession = getSession(token)
  if currentSession == None:
    return personalFunctions.base64encode("<p><a href=\"login\">Please log in</a></p>".encode())
  
  code = request.args.get('code')
  program = personalFunctions.base64decode(code).decode('utf-8').replace("'", "\"")
  
  if "subprocess" in program or "import os" in program or "from os" in program or "pty" in program:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p>We have detected you are trying to gain access to our systems.\nThis incident has been reported.</p>").encode())
  
  output = personalFunctions.runCode(program, currentSession.token)
  
  pageName, chal_id = personalFunctions.base64decode(request.args.get('chal_id')).decode('utf-8').split(' ')

  #print(output)
  #print(yml.data[pageName]['page']['question']["correct"])
  
  if yml.data[pageName]['page']['question']["chal_id"] == chal_id:
    if yml.data[pageName]['page']['question']["correct"] + "\n" == output:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
    else:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())

@app.route('/test/<string:id>', methods=["POST", 'GET']) 
def get_chall(id):
  token = request.cookies.get('token')
  currentSession = getSession(token)

  if currentSession == None:
    return invalidSession()
    
  if accountManager.isAdmin(currentSession.username) == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenges'))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template("challengeTemplate.html", data=yml.data, page=id)

accountManager.getAccounts()
threading.Thread(target=runPeriodically).start()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)
  #sleep(100000000)