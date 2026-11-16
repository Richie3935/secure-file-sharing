from encryption import encrypt_file

# Different content from the original file
modified_data = b"This file has been changed."

# Encrypt using the SAME Fernet key
encrypted_data = encrypt_file(modified_data)

# Save the encrypted replacement
with open("2.txt", "wb") as f:
    f.write(encrypted_data)

print("Modified file encrypted successfully!")
