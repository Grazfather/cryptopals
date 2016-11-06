import unittest

BLOCK_SIZE = 16

def check_pkcs7_padding(s):
    """Raise an exception if the provided string doesn't conform to PKCS7
    padding. Otherwise, return the string with the padding removed.
    This function deliberately has meaningful exception messages to act as an
    oracle."""
    if len(s) % BLOCK_SIZE:
        raise Exception("Not padded to block length")

    pad_byte = ord(s[-1])

    if pad_byte == 0 or pad_byte > BLOCK_SIZE:
        raise Exception("Invalid pad value")

    if s[-pad_byte:] != chr(pad_byte)*pad_byte:
        raise Exception("Invalid padding")

    return True


class TestPkcs7Checker(unittest.TestCase):
    def test_block_length(self):
        self.assertRaises(Exception, check_pkcs7_padding, "less than 1 blk")
        self.assertRaises(Exception, check_pkcs7_padding, "more than 1 block")
        self.assertTrue(check_pkcs7_padding("exactly 1 block!"+"\x10"*BLOCK_SIZE))

    def test_no_padding(self):
        self.assertRaises(Exception, check_pkcs7_padding, "exactly 1 block!")

    def test_padded(self):
        self.assertTrue(check_pkcs7_padding("short block!"+"\x04"*4))

if __name__ == "__main__":
    unittest.main()
