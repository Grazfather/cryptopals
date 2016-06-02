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

def detect_cipher_mode():
    """
    Detect which mode a black box AES encryption routine is using.
    This can be done by providing a block large enough that, even with 5-10
    bytes of random padding on either end, there will be two blocks of
    plaintext that are the same. If the corresponding ciphertexts are the same,
    then we know the mode if ECB, otherwise it's CBC.
    """
    # plaintext is 54 bytes of the same value. This way, no matter the padding
    # (5-10 bytes), we'll have two blocks of all 'A's.
    pt = b"A"*11 + b"A"*32 + b"A"*11
    ct = random_encrypt(pt)

    # Split it into blocks
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

    # Check for duplicates
    if len(blocks) != len(set(blocks)):
        print "ECB!"
    else:
        print "CBC!"

detect_cipher_mode()
