"""Database initialization code"""
import sqlite3
from flask import g

def create_tables():
    """Initialize the database"""
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "AdoptionRequests" (
            "requestID"	INTEGER,
            "FK_userID"	INTEGER,
            "FK_petID"	INTEGER,
            "FK_reviewerID"	INTEGER,
            "time_submitted"	TEXT,
            "status"	TEXT,
            "comments"	TEXT,
            PRIMARY KEY("requestID" AUTOINCREMENT),
            FOREIGN KEY("FK_petID") REFERENCES "Pets"("petID"),
            FOREIGN KEY("FK_reviewerID") REFERENCES "Users"("userID"),
            FOREIGN KEY("FK_userID") REFERENCES "Users"("userID")
        )""")

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS "PetProperties" (
    #         "propertiesID"	INTEGER,
    #         "name" TEXT,
    #         "value" TEXT,
    #         "data_type" TEXT,
    #         PRIMARY KEY("propertiesID" AUTOINCREMENT)
    #     )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Pets" (
            "petID"	INTEGER,
            "name"	TEXT,
            "species"	TEXT,
            "description"	TEXT,
            "image_url" TEXT,
            "FK_adopterID"	INTEGER,
            PRIMARY KEY("petID" AUTOINCREMENT),
            FOREIGN KEY("FK_adopterID") REFERENCES "Users"("userID")
        )""")

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS "PhotoIDs" (
    #         "FK_userID"	INTEGER,
    #         "photo"	BLOB,
    #         FOREIGN KEY("FK_userID") REFERENCES "Users"("userID")
    #     )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Questionnaires" (
            "uniqueID"	INTEGER,
            "question"	TEXT,
            "response"	TEXT,
            "is_approved"	INTEGER,
            "time_submitted"	TEXT,
            "comments"	TEXT,
            "FK_userID"	INTEGER,
            PRIMARY KEY("uniqueID" AUTOINCREMENT),
            FOREIGN KEY("FK_userID") REFERENCES "Users"("userID")
        )""")

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS "Responses" (
    #         "responseID"	INTEGER,
    #         "FK_questionnaireID"	INTEGER,
    #         "question"	TEXT,
    #         "answer"	TEXT,
    #         PRIMARY KEY("responseID" AUTOINCREMENT),
    #         FOREIGN KEY("FK_questionnaireID") REFERENCES "Questionnaires"("uniqueID")
    #     )""")

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS "UserCredentials" (
    #         "userID"	INTEGER,
    #         "password"	TEXT,
    #         "email"	TEXT,
    #         PRIMARY KEY("userID" AUTOINCREMENT)
    #     )""")

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS "Oauth" (
    #         "FK_userID"	INTEGER,
    #         "access_token"	TEXT,
    #         "refresh_token"	TEXT,
    #         "expire_time"	TEXT,
    #         FOREIGN KEY("FK_userID") REFERENCES "Users"("FK_userID")
    #     )
    #     """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Sessions" (
            "sessionID" TEXT PRIMARY KEY,
            "FK_userID" INTEGER,
            "expire_time" TEXT,
            FOREIGN KEY("FK_userID")  REFERENCES "Users"("userID")
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Users" (
            "userID"	INTEGER,
            "username" TEXT,
            "first_name"	TEXT,
            "last_name"	TEXT,
            "password" TEXT,
            "is_admin"	INTEGER,
            PRIMARY KEY("userID" AUTOINCREMENT)
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Notifications" (
            "notificationID"	INTEGER,
            "FK_userID"	INTEGER,
            "message"	TEXT,
            "read"	INTEGER,
            "time_created"	TEXT,
            PRIMARY KEY("notificationID" AUTOINCREMENT),
            FOREIGN KEY("FK_userID") REFERENCES "Users"("userID")
        )""")

    cur.execute("""
        INSERT INTO Users (userID, username, first_name,
        last_name, password, is_admin)
        SELECT 100, "JohnAdopter", "John", "Marks", "password123", 0
        WHERE NOT EXISTS (
        SELECT 1
        FROM Users
        WHERE userID = 100 AND username = "JohnAdopter"
        AND first_name = "John" AND last_name = "Marks"
        AND password = "password123" AND is_admin = 0)
        """)

    cur.execute("""
        INSERT INTO Users (userID, username, first_name,
        last_name, password, is_admin)
        SELECT 101, "EricPetfinderAdmin", "Eric", "Johnson", "unbreakablePassword", 1
        WHERE NOT EXISTS (
        SELECT 1
        FROM Users
        WHERE userID = 101 AND username = "EricPetfinderAdmin"
        AND first_name = "Eric" AND last_name = "Johnson"
        AND password = "unbreakablePassword" AND is_admin = 1);
        """)

    cur.execute("""
        INSERT INTO Users (userID, username, first_name,
        last_name, password, is_admin)
        SELECT 102, "ILoveCats1996", "Sarah", "Howard", "kitten10006", 0
        WHERE NOT EXISTS (
        SELECT 1
        FROM Users
        WHERE userID = 102 AND username = "ILoveCats1996"
        AND first_name = "Sarah" AND last_name = "Howard"
        AND password = "kitten10006" AND is_admin = 0)
        """)

    cur.execute("""
        INSERT INTO Pets (petID, name, species, description, FK_adopterID, image_url)
        SELECT 100, "Ash", "Cat", "Black kitten. Young and playful.", -1, "https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?auto=compress&cs=tinysrgb&w=800"
        WHERE NOT EXISTS (SELECT 1 FROM Pets WHERE petID = 100);
        """)

    cur.execute("""
        INSERT INTO Pets (petID, name, species, description, FK_adopterID, image_url)
        SELECT 101, "Dust", "Dog", "Gray puppy. Energetic and friendly.", -1, "https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg?auto=compress&cs=tinysrgb&w=800"
        WHERE NOT EXISTS (SELECT 1 FROM Pets WHERE petID = 101);
        """)

    cur.execute("""
        INSERT INTO Pets (petID, name, species, description, FK_adopterID, image_url)
        SELECT 102, "John", "Cat", "Senior cat. Spends most of his time sleeping.", -1, "https://images.pexels.com/photos/208984/pexels-photo-208984.jpeg?auto=compress&cs=tinysrgb&w=800"
        WHERE NOT EXISTS (SELECT 1 FROM Pets WHERE petID = 102);
        """)

    cur.execute("""
        INSERT INTO Questionnaires (uniqueID, question,
        response, is_approved, time_submitted, comments, FK_userID)
        SELECT 100, "Do you prefer cats or dogs?", "cats", NULL,
        "2024-11-19 09:37", "N/A", 100
        WHERE NOT EXISTS (SELECT 1 FROM Questionnaires WHERE uniqueID = 100);
        """)

    cur.execute("""
        INSERT INTO Questionnaires (uniqueID, question,
        response, is_approved, time_submitted, comments, FK_userID)
        SELECT 101, "Why do you want to adopt a pet?", "because im cool", NULL,
        "2024-11-19 10:12", "N/A", 100
        WHERE NOT EXISTS (SELECT 1 FROM Questionnaires WHERE uniqueID = 101);
        """)

    cur.execute("""
        INSERT INTO AdoptionRequests (requestID, FK_userID, FK_petID, FK_reviewerID,
        time_submitted, status, comments)
        SELECT 100, 100, 100, -1, "2024-11-19 18:52", "pending", "N/A"
        WHERE NOT EXISTS (SELECT 1 FROM AdoptionRequests WHERE requestID = 100);
        """)

    cur.execute("""
        INSERT INTO AdoptionRequests (requestID, FK_userID, FK_petID, FK_reviewerID,
        time_submitted, status, comments)
        SELECT 101, 100, 101, -1, "2024-11-19 18:56", "pending", "N/A"
        WHERE NOT EXISTS (SELECT 1 FROM AdoptionRequests WHERE requestID = 101);
        """)

    cur.execute("""
        INSERT INTO AdoptionRequests (requestID, FK_userID, FK_petID, FK_reviewerID,
        time_submitted, status, comments)
        SELECT 102, 100, 102, -1, "2024-11-19 19:06", "pending", "test"
        WHERE NOT EXISTS (SELECT 1 FROM AdoptionRequests WHERE requestID = 102);
        """)

    cur.execute("""
        INSERT INTO Sessions (sessionID, FK_userID, expire_time)
        SELECT 100, 100, "2024-11-12 19:15"
        WHERE NOT EXISTS (SELECT 1 FROM Sessions WHERE sessionID = 100);
        """)

    cur.execute("""
        INSERT INTO Notifications (notificationID, FK_userID, message, read, time_created)
        SELECT 100, 100, "Your questionnaire has been approved.", 1, "2024-11-19 15:05"
        WHERE NOT EXISTS (SELECT 1 FROM Notifications WHERE notificationID = 100);
        """)

    conn.commit()
    conn.close()


def get_db():
    """Get the database connection"""
    if 'conn' not in g:
        conn = sqlite3.connect('main.db')
        conn.row_factory = sqlite3.Row
        g.conn = conn

    return g.conn

def close_db():
    """Close the database connection"""
    if 'conn' in g:
        g.conn.commit()
        g.conn.close()
        g.pop('conn')
