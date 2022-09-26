from flask import Flask, jsonify, render_template, request
import time
from sessions import sessions  #, removeInactiveSessions
import accountManager

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():

    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['login'][0]
        password = request.form['login'][1]

        # Check if account information is correct
        if accountManager.checkAccount(username, password) == False:
            return render_template('wrongLogin.html')

        # Create a new session with the username
        currentSession = sessions(username)

    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['login'][0]

        password = request.form['login'][1]
    return render_template('register.html')


@app.route('/admin', methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        if (request.form['button'] == 'shutdown'):
            accountManager.saveAccounts()
            exit(0)

    return render_template('admin.html')


accountManager.getAccounts()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
