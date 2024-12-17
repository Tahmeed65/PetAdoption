"""Basic auth"""


from datetime import datetime, timezone, timedelta
from flask import request, jsonify
from app import app
from db import get_db, close_db


@app.route('/api/basicauth/authenticated', methods=['POST'])
def authenticated():
    """Checks if user is authenticated"""
    session_id = request.json["session_id"]

    conn = get_db()
    cur = conn.cursor()
    query = "SELECT FK_userID FROM Sessions WHERE sessionID = ?"

    cur.execute(query, (session_id,))
    userid = cur.fetchone()
    close_db()

    if userid is None:
        return jsonify({"authenticated": False})

    return jsonify({"authenticated": True, "user_id": userid["userID"]})

@app.route('/api/basicauth/login', methods=['POST'])
def login():
    """Verifies username and password"""
    username = request.json["username"]
    password = request.json["password"]

    conn = get_db()
    cur = conn.cursor()
    query = """
                SELECT userID, first_name, last_name 
                FROM Users 
                WHERE username = ? AND password = ?
            """

    cur.execute(query, (username, password))
    row = cur.fetchone()
    close_db()

    # print(userid)
    if row is None:
        return jsonify({"authenticated": False})

    conn = get_db()
    cur = conn.cursor()
    query = "INSERT INTO Sessions (FK_userID, sessionID, expire_time) VALUES (?,?,?)"
    expire_time = (datetime.now(timezone.utc) + timedelta(seconds=3600)).isoformat()

    session_id = f'{row["userID"]}:{expire_time}'
    cur.execute(query, (row["userID"], session_id, expire_time))
    close_db()

    return jsonify({
        "authenticated": True,
        "user_id": row["userID"],
        "session_id": session_id,
        "name": row["first_name"] + " " + row["last_name"],
    })

@app.route('/api/basicauth/logout', methods=['POST'])
def logout():
    """Logs user out"""
    session_id = request.json["session_id"]

    conn = get_db()
    cur = conn.cursor()
    query = "SELECT FK_userID FROM Sessions WHERE sessionID = ?"

    cur.execute(query, (session_id,))
    userid = cur.fetchone()

    query = "DELETE FROM Sessions WHERE sessionID = ?"
    cur.execute(query, (session_id,))

    close_db()

    if userid is None:
        return jsonify({"authenticated": False})

    return jsonify({"authenticated": True, "user_id": userid["userID"]})
