from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({
        "service": "app1",
        "hostname": socket.gethostname(),
        "message": "Hello from App 1! 👋"
    })

@app.route("/api/data")
def data():
    return jsonify({
        "source": "app1",
        "items": ["Docker", "Compose", "Networking"],
        "status": "ok"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
