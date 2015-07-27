import crypto

best = ""
bestkey = ""
bestscore = 0.0
with open('data/4.txt', 'r') as f:
    for line in f:
        ct = crypto.hex_to_str(line.rstrip())
        for k in range(256):
            s = crypto.xorstring_key(ct, chr(k))
            score = crypto.score_english(s)
            if score > bestscore:
                best = s
                bestkey = k
                bestscore = score

print "Key: '{}' ({}): {}".format(chr(bestkey), bestscore, best)
