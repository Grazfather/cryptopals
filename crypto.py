import base64
from collections import Counter
from itertools import izip


def xorstring(s1, s2):
    return "".join([chr(ord(a) ^ ord(b)) for a, b in izip(s1, s2)])


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
    for c1, c2 in izip(s1, s2):
        for i in range(8):
            if (ord(c1) & 1 << i) != (ord(c2) & 1 << i):
                distance += 1

    return distance
