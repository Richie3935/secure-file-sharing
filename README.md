# Secure Cloud File Sharing System

A Python-based secure cloud file-sharing web application built using Flask, MySQL, MinIO, and cryptographic techniques.

The application provides user authentication, encrypted file storage, integrity verification, owner-based access control, secure downloads, and activity logging.

## Features

### 1. User Authentication
- User registration and login.
- Password hashing using Werkzeug.
- Session-based authentication using Flask.

### 2. Secure File Upload
- Authenticated users can upload files.
- File metadata is stored in MySQL.
- Uploaded files are encrypted before being stored.

### 3. File Integrity Verification
- SHA-256 hashing is used to generate file hashes.
- Hash values are stored in MySQL alongside file metadata.

### 4. File Encryption
- Fernet symmetric encryption using the Python Cryptography library.
- Files are encrypted before cloud storage.
- Files are decrypted when downloaded.

### 5. Cloud/Object Storage
- MinIO provides S3-compatible object storage.
- Encrypted files are stored in a dedicated bucket.

### 6. Access Control
- Owner-based file authorization.
- Users can access and download only their own files.
- Unauthorized access attempts are logged.

### 7. Secure File Download
- Encrypted files are retrieved from MinIO.
- Files are decrypted before being sent to the user.

### 8. Activity Logging
- Records important user activities, including:
  - LOGIN
  - LOGOUT
  - UPLOAD
  - DOWNLOAD
  - ACCESS_GRANTED
  - ACCESS_DENIED

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | User, file metadata and activity storage |
| MinIO | Object storage |
| Fernet / Cryptography | File encryption |
| SHA-256 | File hashing |
| Werkzeug | Password hashing |
| HTML, CSS, JavaScript | Frontend |
| Jinja2 | Flask templates |

## Project Structure

```text
secure-file-sharing/
│
├── app.py
├── database.py
├── encryption.py
├── minio_storage.py
│
├── static/
│   ├── app.js
│   ├── style.css
│   └── auth-bg.png
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── test_encryption.py
├── test_minio.py
├── requirements.txt
├── .gitignore
└── README.md
```

Local runtime files such as `secret.key`, uploaded files, and virtual environments are not included in the repository.

## System Architecture

### File Upload Flow

```text
User
  ↓
Flask Application
  ↓
Authentication Check
  ↓
SHA-256 Hash Generation
  ↓
File Encryption
  ↓
MinIO Object Storage
  ↓
MySQL Metadata Storage
  ↓
Activity Logging
```

### File Download Flow

```text
User
  ↓
Authentication Check
  ↓
Ownership Verification
  ↓
Retrieve Encrypted File from MinIO
  ↓
File Decryption
  ↓
Browser Download
  ↓
Activity Logging
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Richie3935/secure-file-sharing.git
cd secure-file-sharing
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

For Windows:

```cmd
venv\Scripts\activate
```

### 3. Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Otherwise:

```bash
pip install flask mysql-connector-python werkzeug cryptography minio
```

### 4. Configure MySQL

Create the database:

```sql
CREATE DATABASE secure_file_sharing;
USE secure_file_sharing;
```

Create the users table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
```

Create the files table:

```sql
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    owner_id INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_hash VARCHAR(64),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

Create the activity logs table:

```sql
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

Configure your local MySQL connection in `database.py`. Never commit real database credentials.

### 5. Configure MinIO

Start the MinIO server.

Example Windows command:

```cmd
cd C:\minio
minio.exe server C:\minio\data --license C:\minio\minio.license --console-address ":9001"
```

MinIO Console:

```text
http://localhost:9001
```

MinIO API:

```text
http://localhost:9000
```

Create a bucket named:

```text
secure-files
```

The application stores encrypted file objects in this bucket.

Use environment variables and secure credentials instead of default credentials for deployments.

### 6. Run the Application

Ensure MySQL and MinIO are running.

Start Flask:

```bash
python app.py
```

Open the application:

```text
http://127.0.0.1:5000
```

## Testing

The following functionality can be tested through the application:

| Test | Expected Result |
|---|---|
| User registration | New user account is created |
| User login | Authenticated dashboard opens |
| File upload | File is encrypted and stored in MinIO |
| File hashing | SHA-256 hash is stored in MySQL |
| Access control | Only the owner can access the file |
| File download | Original file is decrypted and downloaded |
| Activity logging | User actions are recorded in MySQL |

### Verify Stored File Metadata

```sql
SELECT id, filename, owner_id, file_hash
FROM files;
```

### Verify Activity Logs

```sql
SELECT *
FROM activity_logs
ORDER BY activity_time DESC;
```

## Security Considerations

- Never commit `secret.key` to GitHub.
- Never expose real MySQL or MinIO credentials.
- Keep sensitive configuration files in `.gitignore`.
- Preserve the original encryption key to retain access to existing encrypted files.
- Use strong, unique credentials and secure session configuration.
- Review the implementation and security controls before production deployment.

## Project Status

All eight core modules have been implemented:

- [x] Authentication
- [x] File Upload
- [x] File Hashing
- [x] File Encryption
- [x] MinIO Cloud Storage
- [x] Access Control
- [x] Secure Download
- [x] Activity Logging

---

**Repository:** [Secure Cloud File Sharing System](https://github.com/Richie3935/secure-file-sharing)