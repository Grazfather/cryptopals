import base64


def xorstring(s1, s2):
   return "".join([chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2)])


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
