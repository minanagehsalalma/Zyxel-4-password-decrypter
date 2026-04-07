import base64
import binascii
from Crypto.Cipher import AES

# Keys from inode-/zyxel_password_decrypter
aes_key = "001200054A1F23FB1F060A14CD0D018F5AC0001306F0121C"
aes_iv = "0006001C01F01FC0FFFFFFFFFFFFFFFF"

key = binascii.unhexlify(aes_key)
iv = binascii.unhexlify(aes_iv)

# The target ciphertext from the user
# username admin encrypted-password $4$WliGKvFQ$yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U$
salt = "WliGKvFQ"
value_b64 = "yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U"

def decrypt_zyxel_v4(salt, b64_ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # The script adds '==' for padding if needed, but the value is 80 bytes decoded which is a multiple of 16.
    # Add padding if needed
    missing_padding = len(b64_ciphertext) % 4
    if missing_padding:
        b64_ciphertext += '=' * (4 - missing_padding)
    ciphertext = base64.b64decode(b64_ciphertext)
    decrypted = cipher.decrypt(ciphertext)
    
    print(f"Salt: {salt}")
    print(f"Decrypted (raw): {decrypted}")
    
    # Based on the logic in the script:
    # clear_pass = decrypted.decode('utf-8')[len(str(par.group(1))):decrypted.decode('utf-8').find('\x00')]
    # where par.group(1) is the salt.
    try:
        dec_str = decrypted.decode('utf-8', errors='ignore')
        if salt in dec_str:
            # Find the start of the password (after the salt)
            start_idx = dec_str.find(salt) + len(salt)
            # Find the end of the password (at the first null byte)
            end_idx = dec_str.find('\x00', start_idx)
            if end_idx == -1:
                end_idx = len(dec_str)
            password = dec_str[start_idx:end_idx]
            return password
        else:
            return "Salt not found in decrypted string."
    except Exception as e:
        return f"Error decoding: {e}"

result = decrypt_zyxel_v4(salt, value_b64)
print(f"Decrypted Password: {result}")
