#!/usr/bin/env python3
# coding=utf-8
"""
synopsis: poker exceptions
author: haoranzeus@gmail.com (zhanghaoran)
"""


class PokerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class PokerCardRunOutException(PokerException):
    """
    扑克用光
    """
    def __init__(self, message):
        super(PokerCardRunOutException, self).__init__(message)
