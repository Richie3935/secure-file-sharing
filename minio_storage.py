from minio import Minio
from io import BytesIO

# Connect to MinIO
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Our bucket
BUCKET_NAME = "secure-files"


def upload_to_minio(filename, file_data):

    client.put_object(
        BUCKET_NAME,
        filename,
        BytesIO(file_data),
        length=len(file_data)
    )


def download_from_minio(filename):

    response = client.get_object(
        BUCKET_NAME,
        filename
    )

    data = response.read()

    response.close()
    response.release_conn()

    return data