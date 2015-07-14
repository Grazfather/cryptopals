import base64

import crypto

input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

print "Hex input:"
print input
print "Plaintext:"
print crypto.hex_to_str(input)
print "Encoded"
print crypto.hex_to_base64(input)
