
from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

DATABASE = "authentication.db"


# User Login
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            "error": "Username and password required"
        }), 400

    conn = sqlite3.connect(DATABASE)

    user = conn.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user is None or not check_password_hash(user[1], password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "username": user[0],
        "role": user[2]
    }), 200


# Protected Admin Route
@app.route('/admin', methods=['GET'])
def admin():

    username = request.headers.get('x-username')
    password = request.headers.get('x-password')

    conn = sqlite3.connect(DATABASE)

    user = conn.execute(
        "SELECT role, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user is None or not check_password_hash(user[1], password or ""):
        return jsonify({"error": "Unauthorized"}), 401

    if user[0] != "Admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify({
        "message": "Welcome Admin"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5002)
