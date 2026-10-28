from flask import Flask, render_template, request, redirect, session, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import hashlib
from encryption import encrypt_file, decrypt_file
from minio_storage import upload_to_minio, download_from_minio
from io import BytesIO

from database import get_db_connection


app = Flask(__name__)

# Used for Flask sessions
app.secret_key = "my-secret-key"

# Folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the folder if it doesn't already exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return redirect("/login")

def log_activity(user_id, action, file_id=None, filename=None):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO activity_logs (user_id, action, file_id, filename)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (user_id, action, file_id, filename)
    )

    connection.commit()

    cursor.close()
    connection.close()

# -------------------------
# REGISTER
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Convert password into a secure hash
        password_hash = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """

        try:
            cursor.execute(query, (username, email, password_hash))
            connection.commit()

            cursor.close()
            connection.close()

            return redirect("/login")

        except:
            cursor.close()
            connection.close()

            return "Email already exists."

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        # Check if user exists
        if user:

            # Check password
            if check_password_hash(user["password_hash"], password):

                session["user_id"] = user["id"]
                session["username"] = user["username"]

                log_activity(user["id"], "LOGIN")

                return redirect("/dashboard")

        return "Invalid email or password."

    return render_template("login.html")


# -------------------------
# DASHBOARD
# -------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM files
    WHERE owner_id = %s
    ORDER BY uploaded_at DESC
    """

    cursor.execute(query, (session["user_id"],))

    files = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        files=files
    )

# -------------------------
# FILE UPLOAD
# -------------------------

@app.route("/upload", methods=["POST"])
def upload_file():

    if "user_id" not in session:
        return redirect("/login")

    if "file" not in request.files:
        return "No file selected."

    file = request.files["file"]

    if file.filename == "":
        return "No file selected."

    filename = secure_filename(file.filename)

    # Read original file
    file_data = file.read()

    # Calculate SHA-256 hash of original file
    file_hash = hashlib.sha256(file_data).hexdigest()

    # Encrypt the file
    encrypted_data = encrypt_file(file_data)

    # Save encrypted file
    # Upload encrypted file to MinIO
    upload_to_minio(
        filename,
        encrypted_data
    )

    # Store metadata in MySQL
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO files (filename, owner_id, file_hash)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            filename,
            session["user_id"],
            file_hash
        )
    )

    connection.commit()

    file_id = cursor.lastrowid

    cursor.close()
    connection.close()

    log_activity(
        session["user_id"],
        "UPLOAD",
        file_id,
        filename
    )

    return redirect("/dashboard")

# -------------------------
# ACCESS CONTROL
# -------------------------

@app.route("/check-access/<int:file_id>")
def check_access(file_id):

    # User must be logged in
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Find the requested file
    query = """
    SELECT * FROM files
    WHERE id = %s
    """

    cursor.execute(query, (file_id,))
    file = cursor.fetchone()

    cursor.close()
    connection.close()

    # File doesn't exist
    if not file:
        return "File not found."

    # Check ownership
    if file["owner_id"] != session["user_id"]:

        log_activity(
            session["user_id"],
            "ACCESS_DENIED",
            file["id"],
            file["filename"]
        )

        return "Access denied. You are not authorized to access this file."

    # Owner has access
    log_activity(
        session["user_id"],
        "ACCESS_GRANTED",
        file["id"],
        file["filename"]
    )

    return f"Access granted. You own the file: {file['filename']}"
    
# -------------------------
# DOWNLOAD
# -------------------------

@app.route("/download/<int:file_id>")
def download_file(file_id):

    # Check if user is logged in
    if "user_id" not in session:
        return redirect("/login")

    # Get file information from MySQL
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM files
    WHERE id = %s
    """

    cursor.execute(query, (file_id,))
    file = cursor.fetchone()

    cursor.close()
    connection.close()

    # Check if file exists
    if not file:
        return "File not found."

    # Check if the logged-in user owns the file
    if file["owner_id"] != session["user_id"]:
        return "Access denied. You are not authorized to download this file."

    # Get encrypted file from MinIO
    encrypted_data = download_from_minio(file["filename"])

    # Decrypt the file
    decrypted_data = decrypt_file(encrypted_data)

    # Log successful download
    log_activity(
        session["user_id"],
        "DOWNLOAD",
        file["id"],
        file["filename"]
    )

    # Send the original file to the user
    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=file["filename"]
    )

# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    log_activity(
        session["user_id"],
        "LOGOUT"
    )

    session.clear()

    return redirect("/login")


# -------------------------
# RUN APPLICATION
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)