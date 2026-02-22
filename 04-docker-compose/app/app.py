from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Connect to PostgreSQL with retry logic."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST", "db"),
                port=os.environ.get("DB_PORT", "5432"),
                database=os.environ.get("DB_NAME", "workshop"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASSWORD", "secret")
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Database not ready, retrying... ({retries} attempts left)")
            time.sleep(2)
    raise Exception("Could not connect to database")

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visitors (visited_at) VALUES (NOW())")
    cur.execute("SELECT COUNT(*) FROM visitors")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f"""
    <h1>🐳 Docker Compose Demo</h1>
    <p>This page has been visited <strong>{count}</strong> time(s).</p>
    <p>The count is stored in a PostgreSQL database running in another container!</p>
    <p><a href="/visitors">See all visits</a></p>
    """

@app.route("/visitors")
def visitors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, visited_at FROM visitors ORDER BY visited_at DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    visits_html = "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>" for r in rows)
    return f"""
    <h1>📋 Recent Visits</h1>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>ID</th><th>Timestamp</th></tr>
        {visits_html}
    </table>
    <p><a href="/">Back</a></p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
