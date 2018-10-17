#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil

from dbot.crypto.digest import sha256
from dbot.utils.handle_crypto import (
    str_to_bytes
)
from dbot.utils.handle_data import (
    int_to_little_bytes
)


def pbkdf2(seed: str, dk_len: int) -> bytes:
    """
    Derive one key from a seed.

    :param seed: the secret pass phrase to generate the keys from.
    :param dk_len: the length in bytes of every derived key.
    :return:
    """
    key = b''
    index = 1
    bytes_seed = str_to_bytes(seed)
    while len(key) < dk_len:
        key += sha256(b''.join([bytes_seed, int_to_little_bytes(index)]))
        index += 1
    return key[:dk_len]
