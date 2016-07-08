import os
import urlparse
import urllib
from collections import OrderedDict

import crypto

key = os.urandom(16)

def parse_query(q):
    return urlparse.parse_qs(q)

def profile_for(email):
    # Sanitize
    email = email.replace("&", "").replace("=", "")
    profile = OrderedDict((
        ("email", email),
        ("uid", 10),
        ("role", "user")
    ))
    return urllib.urlencode(profile)

def aes_encrypt_ecb_with_key(pt):
    return crypto.aes_encrypt_ecb(pt, key)

def aes_decrypt_ecb_with_key(ct):
    return crypto.aes_decrypt_ecb(ct, key)

parse_query("foo=bar&baz=qux&zap=zazzl")

profile = profile_for("foo@bar.com")
ct = aes_encrypt_ecb_with_key(profile)
print ct.encode("hex")
pt = aes_decrypt_ecb_with_key(ct)
print pt
