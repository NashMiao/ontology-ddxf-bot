#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct


def int_to_little_bytes(value: int) -> bytes:
    byte_package = struct.pack('<L', value)
    return byte_package


def crypto_str_to_bytes(s: str) -> bytes:
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode('latin-1')
    else:
        return bytes(list(s))


def crypto_bytes_to_str(bs: bytes) -> str:
    return bs.decode('latin-1')
