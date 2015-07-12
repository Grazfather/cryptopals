import base64

input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

print "Hex input:"
print input
print "Plaintext:"
print input.decode('hex')
print "Encoded"
print base64.b64encode(input)
