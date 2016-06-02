import random
import os

import crypto

key = os.urandom(16)

unknown_string = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
                    aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
                    dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
                    YnkK""".decode("base64")


def encrypt_aes_ecb_same_key(data):
    return crypto.aes_encrypt_ecb(data + unknown_string, key)


def break_ecb():
    # Find block size
    pt = b""
    old_l = l = len(encrypt_aes_ecb_same_key(pt))
    while old_l == l:
        pt += b"A"
        l = len(encrypt_aes_ecb_same_key(pt))

    block_size = l - old_l
    print "Block size is {}".format(block_size)

    # Detect mode
    print "Mode is {}".format(crypto.aes_mode_oracle(encrypt_aes_ecb_same_key))

    # Leak out byte by byte
    secret_text = b""  # The secret string so far
    unknown_len = len(unknown_string)
    # Pad to multiple of block_size
    unknown_len = unknown_len/block_size*block_size + (block_size if unknown_len % block_size else 0)

    # Brute force each byte
    while len(secret_text) < len(unknown_string):
        left_pad = b"A" * (unknown_len - len(secret_text) - 1)
        # Encrypt our padding so that the known bytes plus one unknown are in the first chunk
        v = encrypt_aes_ecb_same_key(left_pad)
        # Now brute force this last byte until the whole ct to that point matches
        for i in range(256):
            ct = encrypt_aes_ecb_same_key(left_pad + secret_text + chr(i))
            if ct[0:unknown_len] == v[0:unknown_len]:
                secret_text += chr(i)
                break

    print secret_text


break_ecb()
