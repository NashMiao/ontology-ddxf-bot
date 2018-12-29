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

    def test_bytes_kdf(self):
        dk_len = 64
        seed = b'\x01'
        key_derivation = pbkdf2(seed, dk_len)
        target_key = 'a1cb20470d89874f33383802c72d3c27a0668ebffd81934705ab0cfcbf1a1e3a' \
                     '06dabc1c16aa6baa394cd5d356b6eac101811b0bf78ce32a1ee893cad4b0a83f'
        self.assertEqual(target_key, key_derivation.hex())
        seed = b'\x02'
        key_derivation = pbkdf2(seed, dk_len)
        target_key = '67c60c6612920fc8c68c55d63eadb34b0812235d7b2bf4f13f5692ed8f0cd856' \
                     '5fb807ce100c90d2837ccfc94d8f8ba5d35cd3d6fafcd2f41f245b596e360057'
        self.assertEqual(target_key, key_derivation.hex())
        seed = b'\x01\x02'
        key_derivation = pbkdf2(seed, dk_len)
        target_key = '27704664b7e8ba3c36199f581fa3023f49fd90af918444e2d9477e82565f868a' \
                     '5dbee0a29283512256238cd05870a61c81ccea8a245c8973abc0618df4d3471f'
        self.assertEqual(target_key, key_derivation.hex())


if __name__ == '__main__':
    unittest.main()
