import os
import random

import crypto

def get_random_aes_key():
    return os.urandom(16)

def random_encrypt(data):
    key = get_random_aes_key()

    # Pad both ends with a random amount
    pad_l = b"\0" * random.randint(5, 10)
    pad_r = b"\0" * random.randint(5, 10)
    data = pad_l + data + pad_r

    # Choose cipher
    if random.randint(0, 1):
        return crypto.aes_encrypt_ecb(data, key)
    else:
        iv = get_random_aes_key()
        return crypto.aes_encrypt_cbc(data, key, iv)

print random_encrypt(b"test").encode("hex")
