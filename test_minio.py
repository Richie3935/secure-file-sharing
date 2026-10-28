from minio_storage import upload_to_minio, download_from_minio

data = b"Hello from my Secure Cloud File Sharing System!"

# Upload
upload_to_minio(
    "python_test.txt",
    data
)

print("File uploaded successfully!")

# Download
downloaded_data = download_from_minio(
    "python_test.txt"
)

print("Downloaded data:")
print(downloaded_data.decode())