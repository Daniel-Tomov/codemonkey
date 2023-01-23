from flask import Flask, jsonify, render_template, request, make_response
from sessions import isSession, sessions, userSessions, getSession, removeInactiveSessions
import accountManager
import personalFunctions
import threading
import yml
from time import sleep
from completion import completions, completion, saveCompletions, addNewCompletions
import sendEmail
import verifications
from courseCompletion import courseCompletions, saveCourseCompletions, courseCompletion, addNewCourseCompletions
from flask_compress import Compress
import survey
import logging

# Remove user page access to remove clutter from the console
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# use flask_compress to minify resources to make page loading faster on slower networks
compress = Compress()
def start_app():
    app = Flask(__name__)
    compress.init_app(app)
    return app

# various flask settings to remove whitespace in the HTML file sent to the client after the templating is done.
# also has various security settings to ensure hackers can not use XSS attacks to get a user's session cookie
app = start_app()
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
)

# function that is commonly used to remove a user's cookie once it expires. It also logs them out 
def invalidSession():
  resp = make_response(render_template('redirect.html', redirect_location="/login"))
  resp.set_cookie('token', '')
  return resp

# goes through the "programRuns" folder and removes all files that do not correspond to a session.
def removeOldRuns():
  # get the files
  files = personalFunctions.getFiles('programRuns/')
  for file in files:
    # if the file is not a valid session, valid will stay false and will get deleted below
    valid = False
    for session in userSessions:
      # need to have this filler or git will not upload the folder to github
      if file == "filler.py":
        valid = True
        break
      # break if the file is a valid session.
      if session.token in file:
        valid = True
        break
    if not valid:
      # delete the file
      personalFunctions.deleteFile("programRuns/" + file + ".py")

# this function runs every ten seconds and does a couple of tasks:
#   removes expired sessions
#   removes runs that do not respond to a session token. Because expired sessions were recently removed, files that do not correspond to a session will also be removed.
#   sends verification emails to users that have recently signed up
#   removes varifications from the list of users that have verified their acount
#   saves all user accounts to the database
#   saves all user completions to the database
#   saves all user courseCompletions to the database
#   adds new completions from the challenges.yml file to each user's completions if any are missing in their profile
#   adds new courseCompletions from the challenges.yml file to each user's courseCompletions if there are any missing in their profile
def runPeriodically():
  while True:
    removeInactiveSessions()
    removeOldRuns()
    
    verifications.sendVerification()
    verifications.removeVerifications()
    
    accountManager.saveAccounts()
    saveCompletions()
    saveCourseCompletions()

    addNewCompletions()
    addNewCourseCompletions()

    yml.reloadChallenges()

    sleep(10)

# a commonly used function used to send various security headers back to the user. 
# For example, the ability to access the cookie only from the site is set here. If it was not set, then hackers could use XSS attacks to log a user's cookie with document.cookie in the browser.
def setHeaders(resp, token=""):
  resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
  #resp.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'unsafe-inline'; style-src-elem 'unsafe-inline'"
  resp.headers['X-Content-Type-Options'] = 'nosniff'
  resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
  # set an expiration of the cookie of 10 minutes
  resp.set_cookie('token', token, max_age=600, secure=True, httponly=True, samesite='Strict')
  return resp

# set multiple routes for index.html as user may forget the exact URL
@app.route('/index', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():
  # nothing special needs to be done in index.html because it does not have anything special on it
  token = request.cookies.get('token')
  if isSession(token):
    resp = make_response(render_template('index.html'))
    return setHeaders(resp, token)
  
  return setHeaders(make_response(render_template('index.html')))


@app.route('/login', methods=["POST", "GET"])
def login():
  # Get token from response
  token = request.cookies.get('token')

  # deny access to the login page if the user has a valid token
  if isSession(token) and request.method == "GET" and token != None:
    # Since the user has a valid token, redirect them to the challenges page
    resp = make_response(render_template('redirect.html', redirect_location="/challenge"))
    resp = setHeaders(resp, token)
    return resp
  
  # go here if the request is a POST request. This will only happen when a user is submitting data
  if request.method == "POST":
    username = request.form['uname']
    password = request.form['psw']

    # Check if account information is correct
    if accountManager.checkAccount(username, password) == False:
      return render_template('login.html', wrongPassword=True)

    # Create a new session with the username
    account = accountManager.getAccountByUsername(username)
    currentSession = sessions(account.uid)

    #resp = make_response(render_template('challenge.html', ,))
    resp = make_response(render_template('redirect.html', redirect_location='/challenge'))
    resp = setHeaders(resp, currentSession.token)
    return resp
  # 
  return render_template('login.html')

# route for the register page. Nothing is done here
@app.route('/signUp', methods=["POST", "GET"])
@app.route('/sign_up', methods=["POST", "GET"])
@app.route('/signup', methods=["POST", "GET"])
@app.route('/register', methods=["POST", "GET"])
def register():
  return render_template('register.html')

# this route is accessed only through the AJAX request in register.html
@app.route('/registerForm', methods=["POST", "GET"])
def registerForm():
  # need a try except block here because there could be an error in transporting user information and create an error.
  # there is also the possibility that a hacker could go to the developer console in their browser and make their own request that purposefully breaks the server
  try:
    # base64 decode because they were encoded by the AJAX request.
    username = str(personalFunctions.base64decode(request.args.get('uname')).decode("utf-8"))
    email = str(personalFunctions.base64decode(request.args.get('email')).decode("utf-8"))
    password = str(personalFunctions.base64decode(request.args.get('psw')).decode("utf-8"))
    
    # do checks on email if it is valid. While this is done client side as well, a hacker could go to the developer console in their browser and bypass the checks
    if "@" not in email or "." not in email:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("Please enter a valid email").encode())

    # check if there is a username conflict
    if accountManager.getAccountByUsername(username) != None:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("Sorry, that username exists!").encode())

    # check if there is an email conflict
    if accountManager.getAccountByEmail(email) != None:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("Sorry, that email is in use by another account!").encode())

    # check if the user already registered with the email but has not verified their account
    verification = verifications.getVerificationByEmail(email)
    if verification != None:
      return personalFunctions.base64encode(personalFunctions.replaceNewlines("You have already been sent an email").encode())
    
    # otherwise, create a new instance of the verifications class with the username, email, and password
    verifications.verifications(username, email, password)
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("Please check your email for a code to input. It may be in the spam folder.").encode())
  except:
    # this is returned if there was an error in anything above
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("There has been an error processing your information. Please try again now or later.").encode())

# route for admin page
@app.route('/admin', methods=["POST", "GET"])
def admin():
  # get token from user
  token = request.cookies.get('token')
  # get the instance of the session class. If the session is not valid, getSession() will return None
  currentSession = getSession(token)

  # if it did return None, then the session is invalid
  if currentSession == None:
   return invalidSession()
  # get the instance of the account class based on UID
  account = accountManager.getAccountByUID(currentSession.uid)
  # check if the user is an admin if they are not, then set their token to nothing them out for funsies
  if account.admin == False:
    resp = make_response("You are not an admin")
    resp.set_cookie('token', "")
    return resp
  # if the resquest is a POST request, then do the below functions based on what button was clicked on on the admin page.
  if request.method == "POST":
    if (request.form['button'] == 'saveAccounts'):
      accountManager.saveAccounts()
    elif (request.form['button'] == 'reloadChallenges'):
      yml.reloadChallenges()
    elif (request.form['button'] == 'challengeSubmit'):
      yml.writeChallenges(request.form['challengeQuestions'])
      yml.reloadChallenges()
  resp = make_response(render_template('admin.html', challenges=yml.rawChallengesData))
  resp = setHeaders(resp, currentSession.token)
  return resp

# routes for challenge pages  
@app.route('/challenges', methods=["POST", "GET"])
@app.route('/challenge', methods=["POST", "GET"])
def challenge():
  # get token and if it is not a valid session token, have the user login 
  token = request.cookies.get('token')
  if isSession(token) == False:
    return invalidSession()
  
  # at this point, the session is valid
  currentSession = getSession(token)
  # get account associated with the session
  account = accountManager.getAccountByUID(currentSession.uid)

  # if the account has not completed the presurvey, send them to the presurvey
  # the preSurvey attribute will equal the default survey variable
  if account.preSurvey == accountManager.surveyDict:
    resp = make_response(render_template('redirect.html', redirect_location='/presurvey'))
    resp = setHeaders(resp, currentSession.token)
    return resp
  
  # at this point, the backend is ready to send the challenge page as it will look most of the time. 
  # need to send the username, the data of challenges.yaml, the courseCompletion of the user and if the account is free for templating in challengeTemplate.html
  resp = make_response(render_template('challenge.html', username=currentSession.username, data=yml.data, courseCompletion=courseCompletions[account.uid], free=account.free))
  resp = setHeaders(resp, currentSession.token)
  return resp

# route for the logout page
@app.route('/logout', methods=["POST", "GET"])
def logout():
  # gets the session
  token = request.cookies.get('token')
  currentSession = getSession(token)
  # removes the session to invalidate it
  # first makes sure the session is not invalid to avoid errors
  if currentSession != None:
    currentSession.removeSession()
  return invalidSession()

# 
@app.route('/completions', methods=["POST", 'GET'])
def submitCompletion():
  # there may be an error in transporting the information from the browser to the server. So a try except block is needed
  try:
    token = request.cookies.get('token')
    # check if the user has a valid session token
    # this is because /completions allows reads and writes to a user's courseCompletion information
    currentSession = getSession(token)
    if currentSession == None:
      # "1" can be returned because the AJAX request in the challengeTemplate.html file does not do anything with the response
      return personalFunctions.base64encode("1".encode())
    account = accountManager.getAccountByUID(currentSession.uid)
    # also check if the currentSession has an account
    # this is because /completions allows reads and writes to a user's courseCompletion information
    if account == None:
      return personalFunctions.base64encode("1".encode())

    page = personalFunctions.base64decode(request.args.get('page_id')).decode('utf-8')
    status = personalFunctions.base64decode(request.args.get('status')).decode('utf-8')
    courseCompletions[account.uid][page] = status
  except: 
    # no need to do anything if there is an error
    ""
  # return "1" regardless if there was an error or not
  return personalFunctions.base64encode("1".encode())

# route to recieve user code from challengeTemplate.html
@app.route('/recieve_data', methods=["POST", "GET"])
def recieve_code():
  # get the NotWantedInCode variable
  global NotWantedInCode
  try:
    # check if the session token is valid
    token = request.cookies.get('token')
    currentSession = getSession(token)
    if currentSession == None:
      return personalFunctions.base64encode("<p><a href=\"login\">Please log in</a></p>".encode())
    
    # decode the code argument from base64
    program = personalFunctions.base64decode(request.args.get('code')).decode('utf-8')

    # get the user's code from the request
    output = personalFunctions.base64decode(request.args.get('output')).decode('utf-8').replace("<br>", "\n")
    #print(output)

    # get the name of the page, the question number, and the challlenge ID for later use in the dictionary of completions.
    # this is how the user's code is saved and they can access it later when they refresh the page
    pageName, question, chal_id = personalFunctions.base64decode(request.args.get('chal_id')).decode('utf-8').split(" ")
    completions[currentSession.uid][chal_id][1] = program
    
    # go through different checks to validate user code
    # first check if the submitted ID is the actual ID of the question number for the specific page
    if yml.data[pageName]['page'][question]["chal_id"] == chal_id:
      # check if the output of the user code equal the expected code in challenges.yaml
      if yml.data[pageName]['page'][question]["correct"] + "\n" == output:
        completions[currentSession.uid][chal_id][0] = "complete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p>").encode())
      # if the user is expeced to change the code, then compare thier code to the originial skeleton
      elif yml.data[pageName]['page'][question]["correct"] == "change code":
        if yml.data[pageName]['page'][question]["skeleton"] != program:
          completions[currentSession.uid][chal_id][0] = "complete"
          return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p>").encode())
        else:
          completions[currentSession.uid][chal_id][0] = "uncomplete"
          return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p>").encode())
      # the user can also be expected to have certain strings in their code. This is how it is checked.
      elif yml.data[pageName]['page'][question]["correct"] == "contains":
        # define a count variable that will count the amount of strings the user needs to have versus amount they actually have
        count = 0
        # go through the list of strings in challenges.yaml for the specific question
        for i in yml.data[pageName]['page'][question]["contains"]:
          # if the specific string is in the user's code, then increment count
          if i in program:
            count+=1
        # if the count of the amount of correct strings in the user code is equal to the length of the amount of strings in challenges.yaml, then mark the question as correct
        if count == len(yml.data[pageName]['page'][question]["contains"]):
          return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"correct\">Correct!</p>").encode())
        else:
          return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p>").encode())
      # if none of this is true, then mark the question incomplete
      else:
        completions[currentSession.uid][chal_id][0] = "uncomplete"
        return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">Incorrect! Try again.</p>").encode())
  # if there was an erorr anywhere, when display this error
  except:
    return personalFunctions.base64encode(personalFunctions.replaceNewlines("<p class=\"incorrect\">There has been an erorr in saving your code. Please try again now or later.</p>").encode())

# route for any individual module pages 
@app.route('/challenge/<string:id>', methods=["POST", 'GET']) 
def get_chall(id):

  # validate the user's session token
  token = request.cookies.get('token')
  currentSession = getSession(token)
  if currentSession == None:
    return invalidSession()
  
  # save the instance of the user's account in a variable for later use
  account = accountManager.getAccountByUID(currentSession.uid)
  # if the account does not exist, then log them out
  if account == None:
    resp = make_response(render_template('redirect.html', redirect_location='/logout'))
    resp = setHeaders(resp, currentSession.token)
    return resp
  # try to load the page for the user. If there is an erorr, that means the user has not completed the presurvey
  try:
    return render_template("challengeTemplate.html", data=yml.data, page=id, completion=completions[account.uid], courseCompletion=courseCompletions[account.uid])
  except:
    resp = make_response(render_template('redirect.html', redirect_location='/presurvey'))
    resp = setHeaders(resp, currentSession.token)
    return resp

# route to verify an account
@app.route('/verify/<string:id>', methods=["POST", 'GET']) 
def verify(id):
  # at this point, the user will not have a valid session. Therefore, there is not reason to check it

  # get the instance of the verification class based on the id the user provides
  verify = verifications.getVerificationByID(id)
  # if there is no instance that has a id equal to the one the user provides, then send them back to the register page
  if verify == None:
    resp = make_response(render_template('redirect.html', redirect_location='/register'))
    return resp
  
  # if the user has not verified before, set their verification to true.
  # once it is set to True, the instance of the verification class will be removed after a maximum of 10 seconds by the "runPeriodically" function
  if verify.verified == False:
    verify.setVerified()

    # get the username, email, and hashed password from the instance of the verificaiton class
    username = verify.username
    email = verify.email
    password = verify.password
    account = accountManager.accountManager(username, email, password)
    # return password to the hashed value from the verification object because it was pentahashed when the verificaiton object was made.
    # When creating an instance of the accountManager class, 
    account.password = password

    # Create a new session with the username
    currentSession = sessions(account.uid)
    
    # Create a new completion and courseCompletion for the user
    completion(currentSession.uid)
    courseCompletion(currentSession.uid)

    # if the data in the challenges.yaml has changed, then add that information to the completion and courseCompletions for the user
    addNewCompletions()
    addNewCompletions()

    # send the user to the presurvey page
    resp = make_response(render_template('redirect.html', redirect_location='/presurvey'))
    resp = setHeaders(resp, currentSession.token)
    return resp

# route for the presurvey page
@app.route('/presurvey', methods=["POST", "GET"])
def preSurvey():
  # check the user's session
  token = request.cookies.get('token')
  if isSession(token) == False:
    return invalidSession()

  currentSession = getSession(token)
  account = accountManager.getAccountByUID(currentSession.uid)

  # if the user has completed the presurvey, their preSurvey dictionary will not equal the default one
  if account.preSurvey != accountManager.surveyDict:
    resp = make_response(render_template('redirect.html', redirect_location="/challenges"))
    resp.set_cookie('token', currentSession.token)
    return resp

  # there will be a POST request when the user submits data through the form in presurvey.html
  if request.method == "POST":
    account.preSurvey["feeling"] = request.form.get("feeling")
    account.preSurvey["pursue"] = request.form.get("pursue")
    
    resp = make_response(render_template('redirect.html', redirect_location="/challenges"))
    resp.set_cookie('token', currentSession.token)
    return resp
  
  # at this point, the user will be loading the page normally
  resp = make_response(render_template('presurvey.html'))
  resp = setHeaders(resp, currentSession.token)
  return resp

# route for the postsurvey
@app.route('/postsurvey', methods=["POST", "GET"])
def postSurvey():
  # check the user's session
  token = request.cookies.get('token')
  if isSession(token) == False:
    return invalidSession()

  currentSession = getSession(token)
  account = accountManager.getAccountByUID(currentSession.uid)

  # there is no need to check if the user has completed the survey before because they might want to change their answer.

  # if the request method is POST, that means the user has submit information
  if request.method == "POST":
    account.postSurvey["feeling"] = request.form.get("feeling")
    account.postSurvey["pursue"] = request.form.get("pursue")
    # mark the account as finished with the course.
    account.finished = True
    # the free attribute allows the user to freely go through the course again if they want to.
    # They can get previous questions wrong, it does not matter.
    account.free = 'true'
    
    # because the user completed the post survey, they have completed the course. Therefore, they can see their results
    resp = make_response(render_template('redirect.html', redirect_location="/results"))
    resp.set_cookie('token', currentSession.token)
    return resp
  
  # postsurvey page load with no additional informaiton
  resp = make_response(render_template('presurvey.html'))
  resp = setHeaders(resp, currentSession.token)
  return resp

@app.route('/results', methods=["POST", "GET"])
def results():
  token = request.cookies.get('token')
  if isSession(token) == False:
    return invalidSession()

  currentSession = getSession(token)
  account = accountManager.getAccountByUID(currentSession.uid)

  # if the user tries to access the results page without finishing the course, redirect them back to the challenges page
  if account.finished == False:  
    resp = make_response(render_template('redirect.html', redirect_location="/challenges"))
    resp.set_cookie('token', currentSession.token)
    return resp

  # regular page load for results. Has the account presurvey and postsurvey infromation, and the dictionaries for the individual questions.
  resp = make_response(render_template('results.html', preSurvey=account.preSurvey, postSurvey=account.postSurvey, preFeeling=survey.preFeeling, prePursue=survey.prePursue, postFeeling=survey.postFeeling, postPursue=survey.postPursue))
  resp = setHeaders(resp, currentSession.token)
  return resp

# route for the header
@app.route('/header', methods=["POST", "GET"])
def header():
  # check the user's session
  token = request.cookies.get('token')
  if isSession(token) and request.method == "GET" and token != None:
    currentSession = getSession(token)

    account = accountManager.getAccountByUID(currentSession.uid)
    # the parameters here allow the "Challenges" button to be shown in the header. Also shows the admin page button in the header.  
    # depending on the status of login, the user will be displayed a button to either login or logout
    resp = make_response(render_template('header.html', login=True, admin=account.admin))
    resp = setHeaders(resp, currentSession.token)
    return resp
  return render_template("header.html", login=False)

# route for footer. Nothing special needs to be done
@app.route('/footer', methods=["POST", "GET"])
def footer():
  return render_template("footer.html")

#route for about. Nothing special needs to be done
@app.route('/about', methods=["POST", "GET"])
def about():
  return render_template("about.html")

# route for any 404: Page not found
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

# start the thread that periodically runs the functions in the "runPeriodically" function
threading.Thread(target=runPeriodically).start()

# if "app.py" is the file being run, then go here
if __name__ == "__main__":
  # run the Flask server on port 5555 with debug to False and no reloading when a file is edited
  app.run(host="0.0.0.0", port=5555, debug=True, use_reloader=False)