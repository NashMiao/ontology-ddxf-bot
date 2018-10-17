#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BotException:
    def __init__(self, error: dict):
        super().__init__(error['code'], error['msg'])


class BotError:
    @staticmethod
    def get_error(code: int, msg: str) -> dict:
        error = dict()
        error['code'] = code
        error['msg'] = msg
        return error

    @staticmethod
    def other_error(msg: str) -> dict:
        if isinstance(msg, bytes):
            try:
                msg = msg.decode()
                msg = 'Other Error, ' + msg
            except UnicodeDecodeError:
                msg = 'Other Error'
        return BotError.get_error(60000, msg)
