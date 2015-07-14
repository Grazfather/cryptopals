import crypto

# Sanity test for 'get_hamming_distance'
s1 = "this is a test"
s2 = "wokka wokka!!!"
assert crypto.get_hamming_distance(s1, s2) == 37

ct = crypto.base64_to_str(open('data/6.txt', 'r').read())

# Try to guess the keysize based on the keysize that yields the minimum hamming
# distance
keysize = min(range(2, min(len(ct)/4, 41)),
              key=lambda ks: crypto.get_normalized_hamming_distance(ct, ks, n=4))

# Now break up the ciphertext into blocks on length 'keysize' and transpose so
# that we can do frequency analysis on the result.
blocks = crypto.transpose_str(ct, keysize)

key = ""
for block in blocks:
    keybyte, _, _ = crypto.break_byte_key_english(block)
    key += chr(keybyte)

print "Key: '{}'".format(key)
print crypto.xorstring_key(ct, key)
