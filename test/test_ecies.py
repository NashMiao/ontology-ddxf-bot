#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ecies.utils import generate_eth_key


class EciesTest(unittest.TestCase):
    def test_generate_key(self):
        k = generate_eth_key()
        print(k)
        prvhex = k.to_hex()
        print(prvhex)
        pubhex = k.public_key.to_hex()
        print(pubhex)


if __name__ == '__main__':
    unittest.main()
