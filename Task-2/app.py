
from flask import Flask, request, jsonify
import secrets
import sqlite3

app = Flask(__name__)

DATABASE = "api_keys.db"


# Create database
def create_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Generate API Key
@app.route('/generate-key', methods=['POST'])
def generate_key():

    data = request.get_json(silent=True) or {}
    user = data.get('user')

    if not user:
        return jsonify({"error": "User name required"}), 400

    api_key = secrets.token_hex(16)

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "INSERT INTO api_keys (user, api_key) VALUES (?, ?)",
        (user, api_key)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "API Key generated successfully",
        "user": user,
        "api_key": api_key
    }), 201


# Protected API
@app.route('/protected', methods=['GET'])
def protected():

    api_key = request.headers.get('x-api-key')

    conn = sqlite3.connect(DATABASE)

    result = conn.execute(
        "SELECT user FROM api_keys WHERE api_key = ?",
        (api_key,)
    ).fetchone()

    conn.close()

    if result is None:
        return jsonify({"error": "Invalid API Key"}), 401

    return jsonify({
        "message": "Access granted",
        "user": result[0]
    }), 200


# Show all API Keys
@app.route('/keys', methods=['GET'])
def show_keys():

    conn = sqlite3.connect(DATABASE)

    rows = conn.execute(
        "SELECT user, api_key FROM api_keys"
    ).fetchall()

    conn.close()

    return jsonify([
        {"user": row[0], "api_key": row[1]}
        for row in rows
    ]), 200


if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=5001)
