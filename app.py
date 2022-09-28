from flask import Flask, jsonify, render_template, request
import time
from sessions import sessions, userSessions  #, removeInactiveSessions
import accountManager

app = Flask(__name__)




@app.route('/', methods=["POST", "GET"])
def index():
  
  

  return render_template('index.html', login=True, ipAddress=request.remote_addr)


@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    print(request.form)
    username = request.form['uname']
    password = request.form['psw']
    ipAddress = request.form['ipAddress']

    # Check if account information is correct
    if accountManager.checkAccount(username, password) == False:
      return "Stupid"
      #return render_template('wrongLogin.html')
      
    # Create a new session with the username
    currentSession = sessions(username, ipAddress)
    print(currentSession.token)
    userSessions.append(currentSession)

    return render_template('challenge.html', login=True, ipAddress=ipAddress)
  return render_template('login.html', login=True, ipAddress=request.remote_addr)

@app.route('/register', methods=["POST", "GET"])
def register():
  if request.method == "POST":
    username = request.form['login']
    password = request.form['login']
  return render_template('register.html')


@app.route('/admin', methods=["POST", "GET"])
def admin():
  if request.method == "POST":
    if (request.form['button'] == 'shutdown'):
      accountManager.saveAccounts()
      exit(0)

  return render_template('admin.html')

@app.route('/challenge', methods=["POST", "GET"])
def challenge():


  return render_template('challenge.html')

  
accountManager.getAccounts()

#print(accountManager.accounts)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
