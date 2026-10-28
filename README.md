# Secure Cloud File Sharing System Using Python

A secure cloud file-sharing system built using **Python, Flask, MySQL, Cryptography, and MinIO**.

The project focuses on authentication, file upload, hashing, encryption, cloud/object storage, access control, secure downloading, and activity logging.

## Project Modules

1. **Authentication** — User registration/login, password hashing, Flask sessions.
2. **File Upload** — Logged-in users can upload files; metadata is stored in MySQL.
3. **File Hashing** — SHA-256 hash is generated and stored for file integrity.
4. **File Encryption** — Files are encrypted with Fernet before storage.
5. **Cloud Storage** — MinIO is used as local S3-compatible object storage.
6. **Access Control** — Only the file owner can access/download the file.
7. **Download** — Encrypted files are retrieved, decrypted, and sent to the user.
8. **Activity Logging** — LOGIN, LOGOUT, UPLOAD, DOWNLOAD, ACCESS_GRANTED and ACCESS_DENIED actions are logged.

## Technologies

- Python
- Flask
- MySQL
- MinIO
- `cryptography`
- `mysql-connector-python`
- Werkzeug
- HTML/CSS/Jinja templates

## Project Structure

```text
secure_file_sharing/
├── app.py
├── database.py
├── encryption.py
├── minio_storage.py
├── secret.key
├── requirements.txt
├── README.md
├── uploads/
└── templates/
    ├── register.html
    ├── login.html
    └── dashboard.html
```

> `secret.key` is intentionally not included in GitHub. Never upload it.

## How It Works

### Upload Flow

```text
User → Flask → Authentication Check → SHA-256 Hash
     → Encrypt File → MinIO → Store Metadata in MySQL → Activity Log
```

### Download Flow

```text
User → Flask → Authentication Check → Ownership Check
     → MinIO → Decrypt → Browser Download → Activity Log
```

## Local Setup

Each developer needs their own local Python, MySQL, and MinIO setup.

### 1. Clone the Repository

```cmd
git clone https://github.com/Richie3935/secure-file-sharing.git
cd secure-file-sharing
```

### 2. Create a Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

If `requirements.txt` is not available yet:

```cmd
pip install flask mysql-connector-python werkzeug cryptography minio
```

## MySQL Setup

Create the database and tables:

```sql
CREATE DATABASE secure_file_sharing;
USE secure_file_sharing;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    owner_id INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_hash VARCHAR(64),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    file_id INT NULL,
    filename VARCHAR(255) NULL,
    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Open `database.py` and set your **local** MySQL password:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="secure_file_sharing"
)
```

**Never commit your real MySQL password to GitHub.**

## MinIO Setup

The project uses MinIO as local S3-compatible object storage.

For the current Windows setup:

```cmd
cd C:\minio
minio.exe server C:\minio\data --license C:\minio\minio.license --console-address ":9001"
```

Keep this CMD window running.

Open the MinIO console:

```text
http://localhost:9001
```

The MinIO API is:

```text
http://localhost:9000
```

Create a bucket named:

```text
secure-files
```

The application stores **encrypted** file objects in this bucket.

> For production, MinIO credentials should be stored in environment variables rather than hardcoded.

## Encryption Key

`encryption.py` creates `secret.key` when needed.

Important:

- Do not delete `secret.key` if you need to decrypt existing encrypted files.
- Do not upload `secret.key` to GitHub.
- A different encryption key cannot decrypt files encrypted with the original key.

## Run the Application

Start MinIO first and keep it running:

```cmd
cd C:\minio
minio.exe server C:\minio\data --license C:\minio\minio.license --console-address ":9001"
```

Open another CMD window, go to the project folder, activate the virtual environment, and run:

```cmd
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Basic Testing

### Authentication

1. Register a user.
2. Login.
3. Confirm the dashboard opens.

### Upload

1. Login.
2. Upload a file.
3. Confirm it appears on the dashboard.
4. Confirm an encrypted object appears in the `secure-files` MinIO bucket.

### Hashing

Run:

```sql
SELECT id, filename, owner_id, file_hash FROM files;
```

A SHA-256 hash should be stored for uploaded files.

### Access Control

Run:

```sql
SELECT id, filename, owner_id FROM files;
```

The owner should receive **Access granted**.

A different logged-in user should receive **Access denied**.

### Download

The owner can download the file. The application retrieves the encrypted object from MinIO, decrypts it, and sends the original file to the browser.

### Activity Logging

Run:

```sql
SELECT * FROM activity_logs
ORDER BY activity_time DESC;
```

You should see actions such as:

```text
LOGIN
UPLOAD
ACCESS_GRANTED
ACCESS_DENIED
DOWNLOAD
LOGOUT
```

## Frontend Development

The current frontend uses Flask/Jinja templates in:

```text
templates/
├── register.html
├── login.html
└── dashboard.html
```

A frontend developer can mainly work in the `templates/` folder and add CSS/JavaScript as needed.

The backend Flask routes are in `app.py`. Coordinate before changing route names so existing forms and links continue to work.

## Git Workflow

Before starting work:

```cmd
git pull
```

After making changes:

```cmd
git status
git add .
git commit -m "Describe your changes"
git push
```

If the remote has newer changes:

```cmd
git pull
```

Resolve conflicts if Git reports any, then commit and push.

## Security Notes

Do not commit:

- `secret.key`
- Real MySQL passwords
- Production MinIO credentials
- API keys or other private secrets

Keep sensitive/local files in `.gitignore`.

## Current Status

| Module | Status |
|---|---|
| Authentication | Complete |
| File Upload | Complete |
| File Hashing | Complete |
| File Encryption | Complete |
| Cloud Storage (MinIO) | Complete |
| Access Control | Complete |
| Download | Complete |
| Activity Logging | Complete |

## Project Team

- Himanshu Gidwani
- Pranjal Tanwar
- Abhishek Kumar
- Rachell Gupta
