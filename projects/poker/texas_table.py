#!/usr/bin/env python3
# coding=utf-8
"""
synopsis: texas poker table class
author: haoranzeus@gmail.com (zhanghaoran)
"""


from texaspoker import TexasPoker


class TexasTable:
    def __init__(self, player_count=2):
        self._player_count = player_count
        self._texaspoker = TexasPoker()
        self._player_hole_cards = []

    def shuffle(self):
        """
        洗牌，就是重新弄一个TexasPoker实例
        """
        self._texaspoker = TexasPoker()

    def deal(self):
        """
        发牌
        """
        self._player_hole_cards = []
        for player_id in range(1, self._player_count+1):
            self._player_hole_cards.append(self._texaspoker.pop_hole_cards())

    def get_hole_card(self, player_id):
        """
        根据id获取底牌
        """
        assert isinstance(player_id, int), 'player_id must be int'
        assert player_id <= self._player_count, 'wrong player_id'
        return self._player_hole_cards[player_id]

    def players_rank(self):
        """
        根据每个人的底牌给他们的牌排序
        """


if __name__ == '__main__':
    tb = TexasTable()
    tb.deal()
    print(tb.get_hole_card(1))
