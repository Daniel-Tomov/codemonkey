
from flask import Flask, jsonify, render_template, request
import time
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)