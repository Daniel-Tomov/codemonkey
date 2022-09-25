
from flask import Flask, jsonify, render_template, request
import time
from yml import items
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():

    return render_template('index.html', buttons=items)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)