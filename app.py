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

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE id = ?", (id,))
        result = c.fetchone()  # Fetch one row
        conn.close()
        if result:
            return jsonify({"id": id, "name": result[0]})
        else:
            return jsonify({"error": "User not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({"message": "Welcome to the API. Use /api/users or /api/users/<id> to get data."})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)