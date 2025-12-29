from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE USERS TABLE ----------------
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def create_forms_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ROUTE ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
        # ---------------- CONTACT FORM API ----------------
@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO contact (name, email, message) VALUES (?, ?, ?)",
        (data["name"], data["email"], data["message"])
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ---------------- QUERY FORM API ----------------
@app.route("/query", methods=["POST"])
def query_form():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO query (subject, message) VALUES (?, ?)",
        (data["subject"], data["message"])
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ---------------- FEEDBACK FORM API ----------------
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO feedback (rating, message) VALUES (?, ?)",
        (data["rating"], data["message"])
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


# ---------------- ADD USER (TEMPORARY) ----------------
@app.route("/add-user")
def add_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "admin123")
    )

    conn.commit()
    conn.close()

    return "User added"

@app.route("/view-contact")
def view_contact():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM contact").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/view-query")
def view_query():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM query").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/view-feedback")
def view_feedback():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])



# ---------------- START BACKEND ----------------
if __name__ == "__main__":
    create_users_table()
    create_forms_tables()
    app.run(host="0.0.0.0", port=10000)
