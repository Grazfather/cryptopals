import crypto

input = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

print crypto.str_to_hex(crypto.xorstring_key(input, "ICE"))
