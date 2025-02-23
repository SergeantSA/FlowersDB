from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Path to the SQLite file (assumes 'data.db' is in the same directory as app.py)
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

if __name__ == '__main__':
    app.run(debug=True)