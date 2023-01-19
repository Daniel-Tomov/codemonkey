from flask import Flask, jsonify, render_template, request, make_response
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading
import yml
from time import sleep
from completion import completions, completion, saveCompletions
import sendEmail
import verifications
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
    verifications.sendVerification()
    verifications.removeVerifications()
    accountManager.saveAccounts()
    saveCompletions()
    saveCourseCompletions()
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
    resp = make_response(render_template('redirect.html', login=True, redirect_location="/challenge"))
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
  return render_template('register.html')


@app.route('/registerForm', methods=["POST", "GET"])
def registerForm():
  
  username = personalFunctions.base64decode(request.args.get('uname')).decode("utf-8")
  email = personalFunctions.base64decode(request.args.get('email')).decode("utf-8")
  password = personalFunctions.base64decode(request.args.get('psw')).decode("utf-8")
  
  if accountManager.accountExistsByUsername(username):
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("Sorry, that username exists!").encode())

  if accountManager.accountExistsByEmail(email):
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("Sorry, that email is in use by another account!").encode())


  verification = verifications.getVerificationByEmail(email)
  if verification != None:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("You have already been sent an email").encode())
  
  verifications.verifications(username, email, password)
  return personalFunctions.base64encode(personalFunctions.replaceNewlines("Please check your email for a code to input").encode())

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
  resp = make_response(render_template('challenge.html', data=yml.data, courseCompletion=courseCompletions[account.uid]))
  resp.set_cookie('token', currentSession.token)
  return resp


@app.route('/logout', methods=["POST", "GET"])
def logout():
  token = request.cookies.get('token')
  currentSession = getSession(token)
  
  if currentSession != None:
    currentSession.removeSession()

  return invalidSession()

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
  
  if "subprocess" in program or "import os" in program or "from os" in program or "pty" in program or "open(" in program or "write(" in program or "import" in program:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p>We have detected you are trying to gain access to our systems.\nThis incident has been reported.</p>").encode())

  #print(program)
  output, error = personalFunctions.runCode(program, currentSession.token)


  pageName, question, chal_id = personalFunctions.base64decode(request.args.get('chal_id')).decode('utf-8').split(" ")
  completions[currentSession.uid][chal_id][1] = program


  if "KeyboardInterrupt" in output:
    completions[currentSession.uid][chal_id][0] = "uncomplete"
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Error: Your code took longer than 5 seconds to run. Please try again.</p><p>" + str(output).replace("/home/runner/codemonkey/programRuns/", "") + "</p>").encode())


  if error == 1:
    completions[currentSession.uid][chal_id][0] = "uncomplete"
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Error</p><p>" + str(output).replace("/home/runner/codemonkey/programRuns/", "") + "</p>").encode())

  
  
  if yml.data[pageName]['page'][question]["chal_id"] == chal_id:
    if yml.data[pageName]['page'][question]["correct"] + "\n" == output:
      completions[currentSession.uid][chal_id][0] = "complete"
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
    elif yml.data[pageName]['page'][question]["correct"] == "change code":
      if yml.data[pageName]['page'][question]["skeleton"] != program:
        completions[currentSession.uid][chal_id][0] = "complete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
      else:
        completions[currentSession.uid][chal_id][0] = "uncomplete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())
    elif yml.data[pageName]['page'][question]["correct"] == "contains":
      count = 0
      for i in yml.data[pageName]['page'][question]["contains"]:
        if i in program:
          count+=1
      if count == len(yml.data[pageName]['page'][question]["contains"]):
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p><p>" + output + "</p>").encode())
      else:
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())

    else:
      completions[currentSession.uid][chal_id][0] = "uncomplete"
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p><p>" + output + "</p>").encode())

@app.route('/challenge/<string:id>', methods=["POST", 'GET']) 
def get_chall(id):
  token = request.cookies.get('token')
  currentSession = getSession(token)

  if currentSession == None:
    return invalidSession()
    
  account = accountManager.getAccountByUID(currentSession.uid)
  #print(account)
  if account == None:
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/logout'))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template("challengeTemplate.html", data=yml.data, page=id, completion=completions[account.uid], courseCompletion=courseCompletions[account.uid])

@app.route('/verify/<string:id>', methods=["POST", 'GET']) 
def verify(id):
  verify = verifications.getVerificationByID(id)
  if verify == None:
    return "invalid id"
  
  if verify.verified == False:
    verify.setVerified()

    username = verify.username
    email = verify.email
    password = verify.password
    account = accountManager.accountManager(username, email, password)
    # return password to hashed value because needed to be hashed for verify and not again for account
    account.password = password

    # Create a new session with the username
    currentSession = sessions(account.uid)
    

    # Create a new completion for the user
    #print(currentSession.uid)
    completion(currentSession.uid)
    courseCompletion(currentSession.uid)

    #resp = make_response(render_template('challenge.html', login=True))
    resp = make_response(render_template('redirect.html', login=True, redirect_location='/challenge'))
    resp.set_cookie('token', currentSession.token)
    return resp

@app.route('/header', methods=["POST", "GET"])
def header():
  token = request.cookies.get('token')

  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)


    account = accountManager.getAccountByUID(currentSession.uid)
    resp = make_response(render_template('header.html', login=True, admin=account.admin))
    resp.set_cookie('token', currentSession.token)
    return resp

  return render_template("header.html")
@app.route('/footer', methods=["POST", "GET"])
def footer():
  return render_template("footer.html")

@app.route('/about', methods=["POST", "GET"])
def about():
  return "Christian hasn't made this yet lol"



  return "lol down here"
threading.Thread(target=runPeriodically).start()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5555, debug=True, use_reloader=False)
  #sleep(100000000)