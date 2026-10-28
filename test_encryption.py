from encryption import encrypt_file, decrypt_file

original_data = b"Hello! This is my secret file."

encrypted_data = encrypt_file(original_data)

print("Original:")
print(original_data)

print("\nEncrypted:")
print(encrypted_data)

decrypted_data = decrypt_file(encrypted_data)

print("\nDecrypted:")
print(decrypted_data)