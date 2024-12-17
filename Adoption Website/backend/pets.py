"""Routes relating to pets"""
from datetime import datetime
from flask import jsonify #, session
from app import app
from db import get_db, close_db


@app.route('/api/admin/approve-adoption/<int:admin_id>/<int:userid>/<int:petid>', methods=['POST'])
def approve_adoption_req(admin_id, userid, petid):
    """
    Approves an adoption request
    ---
    parameters:
      - in: path
        name: userid
        schema:
          type: integer
        description: ID of the user
        required: true
      - in: path
        name: petid
        schema:
          type: integer
        description: ID of the pet
        required: true
    responses:
      200:
        description: Adoption request approved successfully
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    adoption_query = """
        UPDATE AdoptionRequests SET 
            status = ?, 
            FK_reviewerID = ?
        WHERE FK_userID = ? AND FK_petID = ?
    """
    cur.execute(adoption_query, ("approved", admin_id, userid, petid))

    pet_query = "UPDATE Pets SET FK_adopterID = ? WHERE petID = ?"
    cur.execute(pet_query, (userid, petid))
    close_db()

    return '{"success": true}'

@app.route('/api/admin/deny-adoption/<int:admin_id>/<int:userid>/<int:petid>', methods=['POST'])
def deny_adoption_req(admin_id, userid, petid):
    """
    Denies an adoption request
    ---
    parameters:
      - in: path
        name: userid
        schema:
          type: integer
        description: ID of the user
        required: true
      - in: path
        name: petid
        schema:
          type: integer
        description: ID of the pet
        required: true
    responses:
      200:
        description: Adoption request denied successfully
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    adoption_query = """
        UPDATE AdoptionRequests SET 
            status = ?, 
            FK_reviewerID = ? 
        WHERE FK_userID = ? AND FK_petID = ?
    """
    cur.execute(adoption_query, ("rejected", admin_id, userid, petid))

    pet_query = "UPDATE Pets SET FK_adopterID = ? WHERE petID = ?"
    cur.execute(pet_query, (userid, petid))
    close_db()

    return '{"success": true}'

@app.route('/api/request-adoption/<int:user_id>/<int:petid>', methods=['POST'])
def request_adoption(user_id, petid):
    """
    Claims a pet for adoption
    ---
    parameters:
      - in: path
        name: petid
        schema:
          type: integer
        description: ID of the pet
        required: true
    responses:
      200:
        description: Pet claimed successfully
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    pet_query = """INSERT INTO AdoptionRequests (FK_userID, FK_petID,
        FK_reviewerID, time_submitted, status, comments) VALUES (?,?,?,?,?,?)"""
    cur.execute(pet_query, (user_id, petid, -1, datetime.now().strftime('%Y-%m-%d %H:%M'),
        "pending", "I really like this one"))

    conn.commit()
    close_db()

    return '{"success": true}'

@app.route('/api/unrequest-adoption/<int:user_id>/<int:petid>', methods=['POST'])
def unrequest_adoption(user_id, petid):
    """
    Unclaims a pet
    ---
    parameters:
      - in: path
        name: petid
        schema:
          type: integer
        description: ID of the pet
        required: true
    responses:
      200:
        description: Pet unclaimed successfully
      401:
        description: Unauthorized
    """

    conn = get_db()
    cur = conn.cursor()
    adoption_query = "DELETE FROM AdoptionRequests WHERE FK_userID = ? AND FK_petID = ?"
    cur.execute(adoption_query, (user_id, petid))

    conn.commit()
    close_db()

    return '{"success": true}'

@app.route('/api/pets', methods=['GET'])
def pets():
    """
    Gets all the pets
    ---
    responses:
      200:
        description: A list of pets
      401:
        description: Unauthorized
    """
    pet_list = []

    conn = get_db()
    cur = conn.cursor()
    pet_query = "SELECT * FROM Pets WHERE FK_adopterID = -1"
    cur.execute(pet_query)
    rows = cur.fetchall()

    for row in rows:
        pet_list.append({
            "petID": row["petID"],
            "name": row["name"],
            "species": row["species"],
            "description": row["description"],
            "image": row["image_url"],
        })

    close_db()

    return jsonify(pet_list)

@app.route('/api/pet/<int:pet_id>', methods=['GET'])
def pet(pet_id):
    """Gets a single pet from its ID"""

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pets WHERE petID = ?", (pet_id,))
    row = cur.fetchone()
    close_db()

    if row is None:
        return jsonify({"status": "pet doesnt exist"}), 400

    return jsonify({
        "petID": row["petID"],
        "name": row["name"],
        "species": row["species"],
        "description": row["description"],
        "image": row["image_url"],
    })
