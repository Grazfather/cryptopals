import crypto

input = crypto.hex_to_str("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")


bestscore = 0
for k in range(256):
    s = crypto.xorstring_key(input, chr(k))
    score = crypto.score_english(s)
    if score > bestscore:
        best = s
        bestscore = score
        bestkey = k

print "Key: '{}' ({}): {}".format(chr(bestkey), bestscore, best)
