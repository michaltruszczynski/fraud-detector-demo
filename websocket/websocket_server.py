from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fraud', methods=['POST'])
def fraud():
    data = request.get_json()
    print(f"Otrzymano fraud: {data}")
    socketio.emit("fraud_alert", data)
    return {"status": "ok"}, 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)