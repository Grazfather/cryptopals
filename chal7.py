from Crypto.Cipher import AES

import crypto

ct = crypto.base64_to_str(open('data/7.txt', 'r').read())

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

pt = cipher.decrypt(ct)
print pt
