"""API routes related to the regular users"""
from datetime import datetime
from flask import request, jsonify #, session
from app import app
from db import get_db, close_db

@app.route('/api/notifications/<int:userid>', methods=['POST'])
def post_notification(userid):
    """
    Sends a notification to a user
    ---
    parameters:
      - in: path
        name: userid
        schema:
          type: integer
        description: ID of the user
        required: true
      - in: body
        name: message
        schema:
          type: string
        description: The message
        required: true
    responses:
      200:
        description: Notification sent successfully
      401:
        description: Unauthorized
    """
    message = request.json['message']
    conn = get_db()
    query = "INSERT INTO Notifications (FK_userID, message, time_created, read) VALUES (?, ?, ?, ?)"
    cur = conn.cursor()
    cur.execute(query, (userid, message, datetime.now().strftime('%Y-%m-%d %H:%M'), 0))
    close_db()

    return '{"success": true}'

@app.route('/api/questionnaire', methods=['GET'])
def get_questionnaire():
    """
    Gets the questions for the questionnaire
    ---
    responses:
      200:
        description: Returns the questions
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
      401:
        description: Unauthorized
    """
    return '["Do you prefer cats or dogs?", "Why do you want to adopt a pet?"]'

@app.route('/api/send-answer', methods=['POST'])
def post_questionnaire():
    """
    Posts the answers to the questionnaire
    ---
    parameters:
      - in: body
        name: answers
        schema:
          type: array
          items:
            type: string
        description: Answers to the questionnaire
        required: true
    responses:
      200:
        description: Answers posted successfully
      401:
        description: Unauthorized
    """
    connection = get_db()
    cur = connection.cursor()

    question = request.json['question']
    answer = request.json['response']
    user_id = request.json['user_id']
    query = """INSERT INTO Questionnaires (question, response, is_approved,
            time_submitted, FK_userID) VALUES (?, ?, ?, ?, ?)"""
    cur.execute(query,
                (question,
                 answer,
                 None,
                 datetime.now().strftime('%Y-%m-%d %H:%M'),
                 user_id))

    close_db()

    return '{"success": true}'

@app.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    """
    Gets the notifications of a user
    ---
    parameters:
      - in: path
        name: userid
        schema:
          type: integer
        description: ID of the user
        required: true
    responses:
      200:
        description: Returns the notifications
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM Notifications WHERE FK_userID = ?"
    cur.execute(query, (user_id,))

    rows = cur.fetchall()

    notif = []

    for row in rows:
        notif.append({
            "notification_id": row["notificationID"],
            "message": row["message"],
            "time": row["time_created"],
            "read": row["read"]
            })
    close_db()
    return jsonify(notif)
    # return '[{"notification_id": 1, "message": "skibidi",
    # "time": "2021-10-01T12:00:00Z", "read": true},
    # {"notification_id": 2, "message": "rizz",
    # "time": "2021-10-01T12:00:00Z", "read": false}]'


@app.route('/api/notifications/read/<int:notification_id>', methods=['PUT'])
def read_notification(notification_id):
    """
    Reads a notification
    ---
    parameters:
      - in: path
        name: notificationid
        schema:
          type: integer
        description: ID of the notification
        required: true
    responses:
      200:
        description: Notification read successfully
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "UPDATE Notifications SET read = ? WHERE notificationID = ?"
    cur.execute(query, (1, notification_id))
    close_db()

    return '{"success": true}'

@app.route('/api/questionnaire-status/<int:user_id>')
def get_quest_status(user_id):
    """
    Gets user questionnaire status
    ---
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        description: ID of the user
        required: true
    responses:
      200:
        description: Questionnaire statuses sent successfully
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM Questionnaires WHERE FK_userID = ?"
    cur.execute(query, (user_id,))

    rows = cur.fetchall()

    questionnaires = []

    for row in rows:
        if row["is_approved"] is None:
            status = "under review"
        elif row["is_approved"] == 1:
            status = "approved"
        else:
            status = "rejected"

        questionnaires.append({
            "questionnaire_id": row["uniqueID"],
            "time": row["time_submitted"],
            "status": status
            })

    close_db()

    return jsonify(questionnaires)

@app.route('/api/adoption-status/<int:user_id>')
def get_adopt_status(user_id):
    """
    Gets user adoption request status
    ---
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        description: ID of the user
        required: true
    responses:
      200:
        description: Adoption request statuses sent successfully
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM AdoptionRequests WHERE FK_userID = ?"
    cur.execute(query, (user_id,))

    rows = cur.fetchall()

    adoption_reqs = []

    for row in rows:
        adoption_reqs.append({
            "request_id": row["requestID"],
            "pet_id": row["FK_petID"],
            "time": row["time_submitted"],
            "status": row["status"]
            })

    close_db()

    return jsonify(adoption_reqs)
