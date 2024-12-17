"""Admin page API"""

from flask import jsonify
from app import app
from db import get_db, close_db

# Assume all these pages are only accessible after a successful admin login

@app.route('/api/adoption-queue', methods=['GET'])
def adoption_queue():
    """
    Gets all the pets in the adoption queue
    ---
    responses:
      200:
        description: Returns the pets in the adoption queue
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
                description: ID of the user who submitted the pet
                example: "9999xyzabc"
              submit_time:
                type: string
                format: date-time
                description: Submission timestamp
                example: "2023-01-01T10:00Z"
              petid:
                type: string
                description: ID of the pet in the queue
                example: "10023fedcba"
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM AdoptionRequests WHERE status = 'pending'")
    # query = "SELECT * FROM AdoptionRequests WHERE status = pending"
    # cur.execute(query, (None,))

    rows = cur.fetchall()

    adoptque = []
    for row in rows:
        # output.append(row["requestID"])
        # output.append(row["FK_userID"])
        # output.append(row["FK_petID"])
        # output.append(row["time_submitted"])
        cur.execute("SELECT first_name, last_name FROM Users WHERE userID = ?", (row["FK_userID"],))
        row2 = cur.fetchone()

        cur.execute("SELECT name, species FROM Pets WHERE petID = ?", (row["FK_petID"],))
        row3 = cur.fetchone()

        adoptque.append({
            "requestID": row["requestID"],
            "userID": row["FK_userID"],
            "user_full_name": row2["first_name"] + " " + row2["last_name"],
            "petID": row["FK_petID"],
            "pet_name": row3["name"],
            "pet_species": row3["species"],
            "submit_time": row["time_submitted"]
        })

    close_db()

    return jsonify(adoptque)

    # return """[{
    #    "userid": "9999xyzabc",
    #    "submit_time": "0000-00-00T00:00Z",
    #    "petid": "10023fedcba"
    #    }]"""  # The brackets indicate that a list of queues will be returned.

@app.route('/api/questionnaire-queue', methods=['GET'])
def questionnaire_queue():
    """
    Gets all the users who have submitted a questionnaire
    ---
    responses:
      200:
        description: Returns the users who have submitted a questionnaire
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
                description: ID of the user who submitted the questionnaire
                example: "9999xyzabc"
              submit_time:
                type: string
                format: date-time
                description: Submission timestamp
                example: "2023-01-01T10:00Z"
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()

    query = """SELECT
                   *
               FROM
                   Questionnaires
               WHERE
                   is_approved IS NULL
               GROUP BY
                   FK_userID
            """
    cur.execute(query)

    rows = cur.fetchall()


    output = []

    for row in rows:
        cur.execute("SELECT first_name, last_name FROM Users WHERE userID = ?", (row["FK_userID"],))
        row2 = cur.fetchone()

        output.append({
            "questionnaireID": row["uniqueID"],
            "userID": row["FK_userID"],
            # "submit_time": row["submit_time"],
            "user_full_name": row2["first_name"] + " " + row2["last_name"]
        })

    close_db()

    return jsonify(output)
    # return """[{
    #     "userid": "9999xyzabc",
    #     "submit_time": "0000-00-00T00:00Z"
    #     }]"""

@app.route('/api/questionnaire/<int:user_id>', methods=['GET'])
def view_user_questionnaire(user_id):
    """
    Gets the questionnaire of a user
    ---
    parameters:
      - in: path
        name: userid
        type: integer
        description: ID of the user
        required: true
    responses:
      200:
        description: Returns the questionnaire
        schema:
          type: array
          items:
            type: object
            properties:
              question:
                type: string
                description: The questionnaire question
                example: "Why do you want to adopt a pet?"
              answer:
                type: string
                description: The user's answer to the question
                example: "I am lonely"
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM Questionnaires WHERE FK_userID=?"
    cur.execute(query, (user_id,))

    rows = cur.fetchall()

    output = []

    if len(rows) == 0:
        return jsonify(output)

    for row in rows:

        output.append({
            "response": row["response"],
            "question": row["question"]
        })

    close_db()

    return jsonify(output)

    # return '[{"question": "Why do you want to adopt a pet?", "answer": "I am lonely"}]'

@app.route('/api/approve-questionnaire/<int:user_id>', methods=['POST'])
def approve_questionnaire(user_id):
    """
    Approves a questionnaire
    ---
    parameters:
      - in: path
        name: userid
        type: integer
        description: ID of the user
        required: true
      - in: body
        name: reason
        description: JSON object containing the reason for approval
        required: false
        schema:
          type: object
          properties:
            reason:
              type: string
              description: Reason for approving the questionnaire
              example: "All requirements met"
    responses:
      200:
        description: Questionnaire approved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    query = "UPDATE Questionnaires SET is_approved = 1 WHERE FK_userID = ?"
    cur.execute(query, (user_id,))
    close_db()

    return '{"success": true}'

@app.route('/api/deny-questionnaire/<int:questionnaire_id>', methods=['POST'])
def deny_questionnaire(questionnaire_id):
    """
    Denies a questionnaire
    ---
    parameters:
      - in: path
        name: userid
        type: integer
        description: ID of the user
        required: true
      - in: body
        name: reason
        description: JSON object containing the reason for denial
        required: false
        schema:
          type: object
          properties:
            reason:
              type: string
              description: Reason for denying the questionnaire
              example: "Incomplete information"
    responses:
      200:
        description: Questionnaire denied successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    query = "UPDATE Questionnaires SET is_approved = 0 WHERE uniqueID = ?"
    cur.execute(query, (questionnaire_id,))
    close_db()

    return '{"success": true}'

@app.route('/api/is-admin/<int:user_id>', methods=['GET'])
def check_admin(user_id):
    """
    Returns whether user is admin
    ---
    parameters:
      - in: path
        name: userid
        type: integer
        description: ID of the user
        required: true
    responses:
      200:
        description: Returns 0 if not admin, 1 if admin
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM Users WHERE userID=?"
    cur.execute(query, (user_id,))

    selected = cur.fetchall()
    result = 0

    for item in selected:
        if item["is_admin"] == 0:
            result = 0
        else:
            result = 1

    close_db()

    output = '{"is_admin": '
    output = output + str(result)
    output = output + "}"

    return output

@app.route('/api/admin/pending-questionnaires', methods=['GET'])
def pending_quests():
    """
    Checks if there are pending user questionnaires
    ---
    responses:
      200:
        description: Questionnaires sent successfully
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Questionnaires WHERE is_approved IS NULL")

    rows = cur.fetchall()

    if len(rows) == 0:
        output = {"pending": "false"}
    else:
        output = {"pending": "true"}

    close_db()

    return jsonify(output)

@app.route('/api/admin/pending-adopts', methods=['GET'])
def pending_adopts():
    """
    Checks if there are pending adoption requests
    ---
    responses:
      200:
        description: Questionnaires sent successfully
      401:
        description: Unauthorized
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM AdoptionRequests WHERE status = 'pending'")

    rows = cur.fetchall()

    if len(rows) == 0:
        output = {"pending": "false"}
    else:
        output = {"pending": "true"}

    close_db()

    return jsonify(output)
  