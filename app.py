from flask import Flask, jsonify, render_template, request, make_response
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading
import yml
from time import sleep
from completion import completions, completion, saveCompletions
from courseCompletion import courseCompletions, saveCourseCompletions, courseCompletion

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True



def invalidSession():
  resp = make_response(render_template('redirect.html', login=True, redirect_location="/login"))
  resp.set_cookie('token', '')
  return resp

def removeOldRuns():
  files = personalFunctions.getFiles('programRuns/')
  for file in files:
    valid = False
    for session in userSessions:
      if file == "filler.py":
        valid = True
        break
      if session.token == file:
        valid = True
        break
    if not valid:
      personalFunctions.deleteFile("programRuns/" + file + ".py")

def runPeriodically():
  while True:
    removeInactiveSessions()
    removeOldRuns()
    accountManager.saveAccounts()
    saveCompletions()
    saveCourseCompletions()
    print(completions)
    print(courseCompletions)
    #print(personalFunctions.convertTime(personalFunctions.time()))
    #print(accountManager.accounts)
    sleep(10)


@app.route('/index', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():

  token = request.cookies.get('token')

  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)


    account = accountManager.getAccountByUID(currentSession.uid)
    resp = make_response(render_template('index.html', login=True, admin=account.admin))
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
    elif request.form['uname'] == "register":
      resp = make_response(render_template('redirect.html', login=True, redirect_location='/register'))
      resp.set_cookie('token', '')
      return resp #hello

    username = request.form['uname']
    password = request.form['psw']

    # Check if account information is correct
    if accountManager.checkAccount(username, password) == False:
      return "Stupid"
      return render_template('wrongLogin.html')

    # Create a new session with the username
    account = accountManager.getAccountByName(username)
    currentSession = sessions(account.uid)

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

    if accountManager.accountExists(username) == True:
      return "Sorry! Account already exists"

    account = accountManager.accountManager(username, password)
    # Create a new session with the username
    currentSession = sessions(account.uid)
    

    # Create a new completion for the user
    #print(currentSession.uid)
    completion(currentSession.uid)
    print(currentSession.uid)
    print(courseCompletion)
    courseCompletion(currentSession.uid)

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

  account = accountManager.getAccountByUID(currentSession.uid)
  
  if account.admin == False:
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
  account = accountManager.getAccountByUID(currentSession.uid)
  resp = make_response(render_template('challenge.html', login=True, admin=account.admin))
  resp.set_cookie('token', currentSession.token)
  return resp


@app.route('/logout', methods=["POST", "GET"])
def logout():
  token = request.cookies.get('token')
  currentSession = getSession(token)
  
  if currentSession != None:
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
    
  account = accountManager.getAccountByUID(currentSession.uid)
  if account.admin == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenges'))
    resp.set_cookie('token', currentSession.token)
    return resp
  
  return render_template("test.html", data=yml.data, courseCompletion=courseCompletions[account.uid])

@app.route('/completions', methods=["POST", 'GET']) 
def submitCompletion():
  token = request.args.get('token')
  currentSession = getSession(token)
  if currentSession == None:
    return personalFunctions.base64encode("1".encode())
  account = accountManager.getAccountByUID(currentSession.uid)
  if account == None:
    return personalFunctions.base64encode("1".encode())

  page = personalFunctions.base64decode(request.args.get('page_id')).decode('utf-8')
  status = personalFunctions.base64decode(request.args.get('status')).decode('utf-8')
  courseCompletions[account.uid][page] = status

  return personalFunctions.base64encode("1".encode())

@app.route('/recieve_data', methods=["POST", "GET"])
def recieve_code():
  token = request.args.get('token')
  currentSession = getSession(token)
  if currentSession == None:
    return personalFunctions.base64encode("<p><a href=\"login\">Please log in</a></p>".encode())
  
  code = request.args.get('code')
  program = personalFunctions.base64decode(code).decode('utf-8')
  
  if "subprocess" in program or "import os" in program or "from os" in program or "pty" in program or "open(" in program or "write(" in program:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p>We have detected you are trying to gain access to our systems.\nThis incident has been reported.</p>").encode())

  #print(program)
  output = personalFunctions.runCode(program, currentSession.token)

  pageName, question, chal_id = personalFunctions.base64decode(request.args.get('chal_id')).decode('utf-8').split(" ")
  completions[currentSession.uid][chal_id][1] = program

  if output[1] == 1:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Erorr</p><p>" + output[0].replace("/home/runner/codemonkey/programRuns/", "") + "</p>").encode())

  output = output[0]
  
  if yml.data[pageName]['page'][question]["chal_id"] == chal_id:
    if yml.data[pageName]['page'][question]["correct"] + "\n" == output:
      completions[currentSession.uid][chal_id][0] = "complete"
      print(completions)
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
    elif yml.data[pageName]['page'][question]["correct"] == "change code":
      if yml.data[pageName]['page'][question]["skeleton"] != program:
        completions[currentSession.uid][chal_id][0] = "complete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
      else:
        completions[currentSession.uid][chal_id][0] = "uncomplete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())
    else:
      completions[currentSession.uid][chal_id][0] = "uncomplete"
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())

@app.route('/test/<string:id>', methods=["POST", 'GET']) 
def get_chall(id):
  token = request.cookies.get('token')
  currentSession = getSession(token)

  if currentSession == None:
    return invalidSession()
    
  account = accountManager.getAccountByUID(currentSession.uid)
  #print(account)
  if account == None or account.admin == False:
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenges'))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template("challengeTemplate.html", data=yml.data, page=id, completion=completions[account.uid], courseCompletion=courseCompletions[account.uid])

threading.Thread(target=runPeriodically).start()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5555, debug=True, use_reloader=False)
  #sleep(100000000)