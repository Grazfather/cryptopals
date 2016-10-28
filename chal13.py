import urlparse
import os

import crypto


def parse_params(params):
    return dict(urlparse.parse_qsl(params))


def encode_params(d):
    # Want to enforce the order, so not using urllib.urlencode
    return "email={}&uid={}&role={}".format(d["email"], d["uid"], d["role"])


def profile_for(email):
    email = email.replace("&", "-").replace("=", "-")
    return {
        "email": email,
        "uid": 10,
        "role": "user"
    }

key = os.urandom(16)

# We want to provide an email that is long enough to stretch over
# a block barrier. Just after that barrier we want a block that says
# "admin".
# email=g@bomb.com&uid=10&role=user
# 0123456789ABCDEF0123456789ABCDEF
email = ""
email += "g@bomb.com"
email += "admin".ljust(16, '\x00')
profile = profile_for(email)
params = encode_params(profile)

print "[*]Encrypting params:\n{}".format(params)
ct = crypto.aes_encrypt_ecb(params, key)
print "[*]Here's your ct:\n{}".format(ct.encode('hex'))

# Snip out the 'admin' block.
admin = ct[16:32]
# Now request a second encoding that has a email whose length puts the
# start of the role into its own block at the end
# email=Much_Long_yes&uid=10&role=user
# 0123456789ABCDEF0123456789ABCDEF
email = "Much_Long_Wow"
profile = profile_for(email)
params = encode_params(profile)

print "[*]Encrypting params:\n{}".format(params)
ct = crypto.aes_encrypt_ecb(params, key)
print "[*]Here's your ct:\n{}".format(ct.encode('hex'))

# Snip off the user and add the admin
attacker_ct = ct[:32] + admin

pt = crypto.aes_decrypt_ecb(attacker_ct, key)
print "[*]Decrypted your ct to:\n{}".format(pt)

print "[*]Created account:\n{}".format(parse_params(pt))
