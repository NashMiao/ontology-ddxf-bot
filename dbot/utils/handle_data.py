#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil


def int_to_little_bytes(value: int) -> bytes:
    bit_length = value.bit_length()
    length = ceil(bit_length / 8)
    byte_package = value.to_bytes(length, 'little', signed=True)
    return byte_package


def int_to_big_bytes(value: int) -> bytes:
    bit_length = value.bit_length()
    length = ceil(bit_length / 8)
    byte_package = value.to_bytes(length, 'big', signed=True)
    return byte_package
