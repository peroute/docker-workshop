from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        # Call app1 by container name — this works because they're on the same network!
        response = requests.get("http://app1:3000/api/data", timeout=5)
        app1_data = response.json()

        return f"""
        <h1>🔗 Networking Demo</h1>
        <h2>I am App 2</h2>
        <p>I just called <strong>App 1</strong> using its container name (<code>http://app1:3000</code>).</p>
        <h3>Response from App 1:</h3>
        <pre>{app1_data}</pre>
        <p style="color: green; font-weight: bold;">
            ✅ Containers can talk to each other by name on the same network!
        </p>
        """
    except requests.exceptions.ConnectionError:
        return f"""
        <h1>❌ Connection Failed</h1>
        <p>Could not reach App 1. Make sure both containers are on the same network!</p>
        """, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
