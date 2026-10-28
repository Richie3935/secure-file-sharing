from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def load_key():

    try:
        with open(KEY_FILE, "rb") as file:
            return file.read()

    except FileNotFoundError:

        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

        return key


key = load_key()

cipher = Fernet(key)


def encrypt_file(file_data):
    return cipher.encrypt(file_data)


def decrypt_file(file_data):
    return cipher.decrypt(file_data)