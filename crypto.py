import base64
from collections import Counter
import itertools
from Crypto.Cipher import AES


def xorstring(s1, s2):
    return "".join([chr(ord(a) ^ ord(b)) for a, b in itertools.izip(s1, s2)])


def xorstring_key(s, key):
    key = (key*(len(s)/len(key) + 1))[:len(s)]
    return xorstring(s, key)


def hex_to_str(s):
    return s.decode('hex')


def hex_to_base64(s):
    return str_to_base64(hex_to_str(s))


def str_to_hex(s):
    return s.encode('hex')


def str_to_base64(s):
    return base64.b64encode(s)


def base64_to_str(s):
    return base64.b64decode(s)


def base64_to_hex(s):
    return str_to_hex(base64_to_str(s))

ENG_FREQ_MAP = {
    " ": 18.28846265,
    "E": 10.26665037,
    "T": 7.51699827,
    "A": 6.53216702,
    "O": 6.15957725,
    "N": 5.71201113,
    "I": 5.66844326,
    "S": 5.31700534,
    "R": 4.98790855,
    "H": 4.97856396,
    "L": 3.31754796,
    "D": 3.28292310,
    "U": 2.27579536,
    "C": 2.23367596,
    "M": 2.02656783,
    "F": 1.98306716,
    "W": 1.70389377,
    "G": 1.62490441,
    "P": 1.50432428,
    "Y": 1.42766662,
    "B": 1.25888074,
    "V": 0.79611644,
    "K": 0.56096272,
    "X": 0.14092016,
    "J": 0.09752181,
    "Q": 0.08367550,
    "Z": 0.05128469,
}


def score_english(s):
    """
    Calculate and return a score for the provided string based on how likely it
    is to be English. Right now it's only a relative scale with no bounding.
    """

    # Get frequency of each character
    count = Counter()
    for c in s:
        count[c.upper()] += 1

    # For each letter in the alphabet, see if this string's frequency % is
    # similar and score on how close it is.
    score = 0.0
    for key, value in ENG_FREQ_MAP.iteritems():
        freq = float(count[key]) / float(len(s)) * 100
        score += freq * value

    return score


def break_byte_key_english(input):
    bestscore = 0
    for k in range(256):
        s = xorstring_key(input, chr(k))
        score = score_english(s)
        if score > bestscore:
            best = s
            bestkey = k
            bestscore = score

    return bestkey, bestscore, best


def get_hamming_distance(s1, s2):
    """
    Calculate the hamming distance between two strings. That is the number of
    different bits.
    """
    distance = 0
    for c1, c2 in itertools.izip(s1, s2):
        for i in range(8):
            if (ord(c1) & 1 << i) != (ord(c2) & 1 << i):
                distance += 1

    return distance


def get_normalized_hamming_distance(s, keysize, n=2):
    """
    Calculate the normalized hamming distance between the first n blocks of len
    'keysize' in the supplied string.
    """
    slices = [s[keysize*i:keysize*(i+1)] for i in range(n)]
    pairs = list(itertools.combinations(slices, 2))
    dist = float(sum([get_hamming_distance(pair[0], pair[1]) for pair in pairs]))/float(len(pairs))
    return float(dist) / float(keysize)


def transpose_str(s, length):
    """
    Get a string and break it up into 'length' strings, where each string i is
    composed of every i-1th character.
    """
    blocks = [s[i:i+length] for i in range(0, len(s), length)]
    transposed = itertools.izip_longest(*blocks, fillvalue="\x00")
    return ["".join(_) for _ in transposed]


def str_to_nlength_blocks(s, length):
    """
    Return a list of slices of string 's' of length 'length', with any leftover
    in the last element.
    """
    if len(s) % length:
        return [s[length*i:length*(i+1)] for i in range(len(s)/length + 1)]
    else:
        return [s[length*i:length*(i+1)] for i in range(len(s)/length)]


def get_padded(s, length):
    """
    Returns a new string padded to a multiple of the block length using PKCS#7.
    """
    pad = length - len(s) % length
    if pad == length:
        return s
    else:
        return s + chr(pad) * pad


def aes_decrypt_ecb(ct, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ct)


def aes_encrypt_ecb(pt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(get_padded(pt, AES.block_size))


def aes_decrypt_block(ct, key):
    ct = ct[:AES.block_size]
    return aes_decrypt_ecb(ct, key)


def aes_encrypt_block(pt, key):
    pt = pt[:AES.block_size]
    return aes_encrypt_ecb(pt, key)


def aes_decrypt_cbc(ct, key, iv):
    blocks = str_to_nlength_blocks(ct, AES.block_size)
    feed = iv
    pt = ""
    for block in blocks:
        ptb = aes_decrypt_block(block, key)
        ptb = xorstring_key(ptb, feed)
        feed = block
        pt += ptb

    return pt


def aes_encrypt_cbc(pt, key, iv):
    pt = get_padded(pt, AES.block_size)
    blocks = str_to_nlength_blocks(pt, AES.block_size)
    feed = iv
    ct = ""
    for block in blocks:
        input = xorstring_key(block, feed)
        ctb = aes_encrypt_block(input, key)
        feed = ctb
        ct += ctb

    return ct


def aes_mode_oracle(enc_func):
    """
    Detect which mode a black box AES encryption routine is using.  This can be
    done by providing a plaintext large enough that there will be at least two
    blocks of plaintext that are the same. If the corresponding ciphertexts
    contain identical blocks, then we know the mode if ECB, otherwise it's CBC.
    """
    pt = b"A"*64
    ct = enc_func(pt)

    # Split it into blocks
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

    # Check for duplicates
    if len(blocks) != len(set(blocks)):
        return "ECB"
    else:
        return "CBC"
