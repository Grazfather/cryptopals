import crypto

bl = 20

# Standard test
b = crypto.get_padded("YELLOW SUBMARINE", bl)
print repr(b)

# Exactly the block length
b = crypto.get_padded("YELLOW SUBMARINE!!!!", bl)
print repr(b)

# More than one block
b = crypto.get_padded("YELLOW SUBMARINE!!!!!", bl)
print repr(b)
