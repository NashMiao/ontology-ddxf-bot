#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from dbot.crypto.kdf import pbkdf2
from dbot.utils.handle_crypto import get_random_hex_str


class KdfTest(unittest.TestCase):
    def test_pbkdf2(self):
        seed = get_random_hex_str(24)
        dk_len = 10
        key_derivation = pbkdf2(seed, dk_len)
        self.assertEqual(dk_len, len(key_derivation))
        dk_len = 24
        key_derivation = pbkdf2(seed, dk_len)
        self.assertEqual(dk_len, len(key_derivation))
        dk_len = 32
        key_derivation = pbkdf2(seed, dk_len)
        self.assertEqual(dk_len, len(key_derivation))
        dk_len = 64
        key_derivation = pbkdf2(seed, dk_len)
        self.assertEqual(dk_len, len(key_derivation))

    def test_aa(self):
        dk_len = 64
        seed = b'\x01'
        key_derivation = pbkdf2(seed, dk_len)
        print(key_derivation.hex())
        seed = b'\x02'
        key_derivation = pbkdf2(seed, dk_len)
        print(key_derivation.hex())
        seed = b'\x01\x02'
        key_derivation = pbkdf2(seed, dk_len)
        print(key_derivation.hex())


if __name__ == '__main__':
    unittest.main()
