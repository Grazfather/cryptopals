import random
import os

import crypto

key = os.urandom(16)

unknown_string = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
                    aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
                    dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
                    YnkK""".decode("base64")
random_string = os.urandom(random.randint(1, 64))


def encrypt_aes_ecb_same_key(data):
    return crypto.aes_encrypt_ecb(random_string + data + unknown_string, key)


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

    # Find out the length of the random string
    # -- Keep adding a character until finally the size grows. The blocks at
    #    that point don't need padding, and so the length of the random string
    #    is the length of ct - the random string and the added length
    unknown_len = len(unknown_string)
    old_l = l = len(encrypt_aes_ecb_same_key(b"")) - unknown_len
    while old_l == l:
        pt += b"A"
        l = len(encrypt_aes_ecb_same_key(pt))
    random_len = l - len(pt) - unknown_len - block_size + 2 # +2 to compensate for extra 'A' and longer l

    # Leak out byte by byte
    secret_text = b""  # The secret string so far
    # Pad to multiple of block_size
    unknown_len = unknown_len/block_size*block_size + (block_size if unknown_len % block_size else 0)
    # Pad the uncontrolled random text to a block size
    left_pad_len = random_len/block_size*block_size + (block_size if random_len % block_size else 0)
    left_pad = b"L" * (left_pad_len - random_len)
    total_len = unknown_len + left_pad_len

    # Brute force each byte
    while len(secret_text) < len(unknown_string):
        # We control a 'center' pad. We don't care about the random on the
        # left as long as it ends on a block barrier, so consider it extra padding
        center_pad = b"A" * (unknown_len - len(secret_text) - 1)
        # Encrypt our padding so that the known bytes plus one unknown are in the first chunk
        v = encrypt_aes_ecb_same_key(left_pad + center_pad)
        #import pdb; pdb.set_trace()
        # Now brute force this last byte until the whole ct to that point matches
        for i in range(256):
            ct = encrypt_aes_ecb_same_key(left_pad + center_pad + secret_text + chr(i))
            if ct[0:total_len] == v[0:total_len]:
                secret_text += chr(i)
                break

    print secret_text


break_ecb()
