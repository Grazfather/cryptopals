from Crypto.Cipher import AES

import crypto

# Since we are keeping it in hex, it's double the actual block length
BLOCK_LENGTH = 32
cts = []
with open('data/8.txt', 'r') as f:
    for line in f:
        cts.append(line.rstrip())

for i, ct in enumerate(cts, start=1):
    blocks = crypto.str_to_nlength_blocks(ct, BLOCK_LENGTH)
    if blocks[-1] == '':
        blocks = blocks[:-1]

    if len(blocks) != len(set(blocks)):
        print "Found ECB candidate: line {}".format(i)
        print ct
        seen = set()
        rb = None
        for block in blocks:
            if block in seen:
                rb = block
                break
            else:
                seen.add(block)
        print "(First) Repeated block: {}".format(rb)
