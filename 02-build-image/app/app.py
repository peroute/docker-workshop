from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello from Docker! 🐳</h1><p>This app is running inside a container.</p>"

@app.route("/info")
def info():
    return jsonify({
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "time": datetime.datetime.now().isoformat(),
        "message": "This info comes from inside the container!"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "my-flask-app"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
