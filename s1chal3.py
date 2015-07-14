import crypto

input = crypto.hex_to_str("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")


key, score, string = crypto.break_byte_key_english(input)

print "Key: '{}' ({}): {}".format(chr(key), score, string)
