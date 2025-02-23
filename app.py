from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Path to the SQLite file
DB_PATH = "data.db"

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = [{'id': row[0], 'name': row[1]} for row in c.fetchall()]
        conn.close()
        return jsonify(users)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Add a root route to avoid 404 on /
@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({"message": "Welcome to the API. Use /api/users to get data."})

if __name__ == '__main__':
    # Get the port from the environment variable 'PORT', default to 5000 if not set
    port = int(os.getenv("PORT", 5000))
    # Bind to 0.0.0.0 to make it accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)