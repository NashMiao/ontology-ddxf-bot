#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import randint

from ecdsa.curves import SECP256k1

from ecdsa.ellipticcurve import Point

from ecdsa.util import (
    string_to_number,
    number_to_string
)

from ecdsa.keys import (
    SigningKey,
    VerifyingKey,
    BadSignatureError
)

from dbot.crypto.aes import AESHandler
from dbot.crypto.kdf import pbkdf2

from dbot.exception.bot_exception import (
    BotException,
    BotError
)


class ECDSA:
    @staticmethod
    def generate_private_key():
        private_key = SigningKey.generate(SECP256k1)
        return private_key.to_string()

    @staticmethod
    def ec_get_public_key_by_private_key(private_key: bytes):
        if not isinstance(private_key, bytes):
            raise BotException(BotError.invalid_private_key)
        if len(private_key) != 32:
            raise BotException(BotError.invalid_private_key)
        private_key = SigningKey.from_string(string=private_key, curve=SECP256k1)
        public_key = private_key.get_verifying_key().to_string()
        return public_key

    @staticmethod
    def generate_signature(private_key: bytes, msg: bytes):
        if not isinstance(private_key, bytes):
            raise BotException(BotError.invalid_private_key)
        if len(private_key) != 32:
            raise BotException(BotError.invalid_private_key)
        private_key = SigningKey.from_string(string=private_key, curve=SECP256k1)
        signature = private_key.sign(msg)
        return signature

    @staticmethod
    def verify_signature(public_key: bytes, signature: bytes, msg: bytes):
        if not isinstance(public_key, bytes):
            raise BotException(BotError.invalid_public_key)
        if len(public_key) != 64:
            raise BotException(BotError.invalid_public_key)
        public_key = VerifyingKey.from_string(string=public_key, curve=SECP256k1)
        try:
            result = public_key.verify(signature, msg)
        except BadSignatureError:
            result = False
        return result


class ECIES:
    @staticmethod
    def encrypt_with_cbc_mode(plain_text: bytes, public_key: bytes) -> (bytes, bytes, bytes):
        if not isinstance(public_key, bytes):
            raise BotException(BotError.invalid_public_key)
        if len(public_key) != 64:
            raise BotException(BotError.invalid_public_key)
        r = randint(1, SECP256k1.order)
        g_tilde = r * SECP256k1.generator
        h_tilde = r * VerifyingKey.from_string(string=public_key, curve=SECP256k1).pubkey.point
        str_g_tilde_x = number_to_string(g_tilde.x(), SECP256k1.order)
        str_g_tilde_y = number_to_string(g_tilde.y(), SECP256k1.order)
        encode_g_tilde = b''.join([b'\x04', str_g_tilde_x, str_g_tilde_y])
        str_h_tilde_x = number_to_string(h_tilde.x(), SECP256k1.order)
        seed = b''.join([encode_g_tilde, str_h_tilde_x])
        aes_key = pbkdf2(seed, 32)
        aes_iv, cipher_text = AESHandler.aes_cbc_encrypt(plain_text, aes_key)
        return aes_iv, encode_g_tilde, cipher_text

    @staticmethod
    def decrypt_with_cbc_mode(cipher_text: bytes, private_key: bytes, iv: bytes, encode_g_tilde: bytes):
        if not isinstance(private_key, bytes):
            raise BotException(BotError.invalid_private_key)
        if len(private_key) != 32:
            raise BotException(BotError.invalid_private_key)
        str_g_tilde_x = encode_g_tilde[1:33]
        str_g_tilde_y = encode_g_tilde[33:65]
        g_tilde_x = string_to_number(str_g_tilde_x)
        g_tilde_y = string_to_number(str_g_tilde_y)
        g_tilde = Point(SECP256k1.curve, g_tilde_x, g_tilde_y, SECP256k1.order)
        h_tilde = g_tilde * SigningKey.from_string(string=private_key, curve=SECP256k1).privkey.secret_multiplier
        seed = b''.join([encode_g_tilde, number_to_string(h_tilde.x(), SECP256k1.order)])
        aes_key = pbkdf2(seed, 32)
        plain_text = AESHandler.aes_cbc_decrypt(cipher_text, iv, aes_key)
        return plain_text

    @staticmethod
    def encrypt_with_gcm_mode():
        pass
