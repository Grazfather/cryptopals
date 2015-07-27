import crypto

ct = crypto.base64_to_str(open('data/7.txt', 'r').read())

key = "YELLOW SUBMARINE"
pt = crypto.aes_decrypt_ecb(ct, key)
print pt
