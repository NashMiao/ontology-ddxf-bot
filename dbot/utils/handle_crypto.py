#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Cryptodome import Random


def str_to_bytes(s: str) -> bytes:
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode('latin-1')
    else:
        return bytes(list(s))


def bytes_to_str(bs: bytes) -> str:
    return bs.decode('latin-1')


def get_random_bytes(length: int) -> bytes:
    return Random.get_random_bytes(length)


def get_random_hex_str(length: int) -> str:
    return Random.get_random_bytes(length).hex()[:length]
