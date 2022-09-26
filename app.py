
from flask import Flask, jsonify, render_template, request
import time
from sessions import *
import accountManager

app = Flask(__name__)



@app.route('/', methods=["POST", "GET"])
def index():

    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():

  # Create a new session with the username
  sessions('Daniel_Tomov', 'Password1234')

  
  return render_template('index.html')

accountManager.getAccounts()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)