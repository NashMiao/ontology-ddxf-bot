#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil


def pbkdf2(seed: str, dk_len: int):
    digest_size = 32
    block_num = ceil(dk_len / (8 * digest_size))
    for i in range(block_num):
        index = i * digest_size
