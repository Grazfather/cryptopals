import crypto

ct = crypto.base64_to_str(open('data/10.txt', 'r').read())
key = "YELLOW SUBMARINE"
iv = '\x00' * 16

# Decrypt
pt = crypto.aes_decrypt_cbc(ct, key, iv)
print pt

# Re-encrypt
new_ct = crypto.aes_encrypt_cbc(pt, key, iv)

if ct == new_ct:
    print "Success!"
else:
    print "Encryption/Decryption failed!"
