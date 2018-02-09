#!/usr/bin/env python3
# coding=utf-8
"""
synopsis: poker class
author: haoranzeus@gmail.com (zhanghaoran)
"""
import random

from exceptions import PokerCardRunOutException


class Poker:
    SUITS = ['club', 'diamond', 'heart', 'spade']
    POINTS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    POINT_WEIGHT = {
        '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
        '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13
    }

    def __init__(self):
        self.cards = []
        for suit in self.SUITS:
            for point in self.POINTS:
                card = [suit, point]    # a card
                self.cards.append(card)

    def pop_card(self):
        """
        发一张牌
        """
        if len(self.cards) == 0:
            raise PokerCardRunOutException('card run out')
        index = random.randint(0, len(self.cards)-1)
        card = self.cards.pop(index)
        return card

    @classmethod
    def get_largest_card(cls, cards):
        """
        给出牌的列表，返回最大的一张
        """
        weight_tmp = 0
        card_tmp = None
        for card in cards:
            if cls.POINT_WEIGHT[card[1]] > weight_tmp:
                weight_tmp = cls.POINT_WEIGHT[card[1]]
                card_tmp = card
        return card_tmp


if __name__ == '__main__':
    poker = Poker()
    print(poker.pop_card())
    cards = []
    for i in range(0, 3):
        cards.append(poker.pop_card())
    print(cards)
    card = Poker.get_largest_card(cards)
    print(card)
