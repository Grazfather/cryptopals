import os

import crypto

key = os.urandom(16)
iv = os.urandom(16)


def create_order(userdata):
    # TODO: Escape ; and =
    userdata = userdata.replace(";", "SEMICOLON").replace("=", "EQUALS")
    text = "comment1=cooking%20MCs;userdata={};comment2=%20like%20a%20pound%20of%20bacon".format(userdata)

    # Pad to 16 byte barrier (function does it for us)
    # Encrypt
    ct = crypto.aes_encrypt_cbc(text, key, iv)
    return ct

def check_admin(ct):
    pt = crypto.aes_decrypt_cbc(ct, key, iv)
    fields = pt.split(";")
    d = {}
    tuples = [field.split("=") for field in fields]
    for tup in tuples:
        if len(tup) == 2:
            d[tup[0]] = tup[1]

    print pt
    print d

    if "admin" in d and d["admin"] == "true":
        return True

    return False

ud = "AAAABBBBCCCCDDDDEEEEF:admin<true"

ct = create_order(ud)

# Toggle bits in the first userdata block to toggle the same one in the second.
# This will switch the '<'` to a '=' and the ':' to a ';'
ct = ct[:0x25] + chr(ord(ct[0x25]) ^ 1) + ct[0x26:] # Does first ; nicely
ct = ct[:0x2B] + chr(ord(ct[0x2B]) ^ 1) + ct[0x2C:] # Does = nicely

if check_admin(ct):
    print("Admin check passed!")
else:
    print("No admin")
