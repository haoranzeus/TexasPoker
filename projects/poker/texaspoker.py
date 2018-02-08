#!/usr/bin/env python3
# coding=utf-8
"""
synopsis: texas poker class
author: haoranzeus@gmail.com (zhanghaoran)
"""

from pokerdeck import Poker


class TexasPoker(Poker):
    CARD_TYPE = [
        'Royal Flush',          # 0. 同花大顺
        'Straight Flush',       # 1. 同花顺
        'Four of a Kind',       # 2. 四条
        'Fullhouse',            # 3. 葫芦
        'Flush',                # 4. 同花
        'Straight',             # 5. 顺子
        'Three of a kind',      # 6. 三条
        'Two Pairs',            # 7. 两对
        'one Pair',             # 8. 一对
        'high card'             # 9. 高牌
    ]

    def __init__(self):
        super(TexasPoker, self).__init__()
        self._flops = []
        self._turn = None
        self._rever = None

    def pop_hole_cards(self):
        hole_cards = []
        hole_cards.append(self.pop_card())
        hole_cards.append(self.pop_card())
        return hole_cards

    def pop_flop(self):
        """
        前三张公共牌
        """
        self._flops.append(self.pop_card())
        self._flops.append(self.pop_card())
        self._flops.append(self.pop_card())
        return self._flops

    def pop_turn(self):
        """
        第四张公共牌
        """
        self._turn = self.pop_card()
        return self._turn

    def pop_rever(self):
        """
        第五张公共牌
        """
        self._rever = self.pop_card()
        return self._rever

    def merge_cards(self, hole_cards):
        """
        将底牌、翻牌、转牌、河牌合到一起
        """
        cards = hole_cards + self._flops
        cards.append(self._turn)
        cards.append(self._rever)
        return cards

    def order_by_suit(self, hole_cards):
        """
        按花色理牌
        """
        cards = self.merge_cards(hole_cards)
        cards_ordered = {
            'club': [],
            'diamond': [],
            'heart': [],
            'spade': []
        }
        for card in cards:
            cards_ordered[card[0]].append(card)
        return cards_ordered

    def _get_weights_list(self, hole_cards, reverse=False):
        """
        获取一手牌的权重列表
        """
        cards = self.merge_cards(hole_cards)
        return self._get_weights(cards, reverse=reverse)

    def _get_weights(self, cards, reverse=False):
        """
        给出一个牌的列表，给出权重值的列表
        """
        weights = [self.POINT_WEIGHT[card[1]] for card in cards]
        weights.sort(reverse=reverse)
        return weights

    def _if_straight(self, weights):
        """
        给出排序好的权重值列表，判断是否为顺子
        """
        if len(weights) < 5:
            return False
        straight_len = 1
        tmp = weights.pop()
        while True:
            try:
                current_weight = weights.pop()
                if tmp - current_weight == 1:
                    straight_len += 1
                    if straight_len >= 5:
                        return True
                else:
                    straight_len = 1
                tmp = current_weight
            except IndexError:
                return False

    def is_royal_flush(self, hole_cards):
        """
        判断是否为同花大顺，如果是True，否则返回False
        """
        cards_by_suit = self.order_by_suit(hole_cards)
        for cards in cards_by_suit.values():
            if len(cards) < 5:
                continue
            weights = self._get_weights(cards)
            if weights[-1] != self.POINT_WEIGHT['A']:
                continue
            if self._if_straight(weights):
                return True
        return False

    def is_straight_flush(self, hole_cards):
        """
        判断是否为同花顺
        """
        cards_by_suit = self.order_by_suit(hole_cards)
        for cards in cards_by_suit.values():
            if len(cards) < 5:
                continue
            weights = self._get_weights(cards)
            # 如果A存在，A2345也算顺子
            if self.POINT_WEIGHT['A'] in weights:
                weights.insert(0, 0)
            if self._if_straight(weights):
                return True
        return False

    def _statistic_weights(self, weights):
        """
        针对每种权重值统计个数
        """
        statistics = {}
        while True:
            try:
                weight = weights.pop()
                if weight not in statistics.keys():
                    statistics[weight] = 1
                else:
                    statistics[weight] += 1
            except IndexError:
                break
        return statistics

    def is_four_of_a_kind(self, hole_cards):
        """
        判断是否为四条
        """
        weights = self._get_weights_list(hole_cards, reverse=True)
        weights_statistic = self._statistic_weights(weights)
        if 4 in weights_statistic.values():
            return True
        else:
            return False

    def is_fullhouse(self, hole_cards):
        """
        判断是否为葫芦
        """
        weights = self._get_weights_list(hole_cards, reverse=True)
        weights_statistic = self._statistic_weights(weights)
        weights_statistic_values = list(weights_statistic.values())
        treble_weight_count = weights_statistic_values.count(3)
        double_weight_count = weights_statistic_values.count(2)
        if treble_weight_count == 0:
            return False
        if treble_weight_count + double_weight_count >= 2:
            return True
        else:
            return False

    def is_flush(self, hole_cards):
        """
        判断是否为同花
        """
        cards_by_suit = self.order_by_suit(hole_cards)
        for cards in cards_by_suit.values():
            if len(cards) >= 5:
                return True
        return False

    def is_straight(self, hole_cards):
        """
        判断是否为顺子
        """
        weights = self._get_weights_list(hole_cards)
        weights = list(set(weights))    # 去重
        # 如果A存在，A2345也算顺子
        if self.POINT_WEIGHT['A'] in weights:
            weights.insert(0, 0)
        if self._if_straight(weights):
            return True
        return False

    def is_three_of_a_kind(self, hole_cards):
        """
        判断是否为三条
        """
        weights = self._get_weights_list(hole_cards, reverse=True)
        weights_statistic = self._statistic_weights(weights)
        if 3 in weights_statistic.values():
            return True
        else:
            return False

    def is_two_paires(self, hole_cards):
        """
        判断是否为两对
        """
        weights = self._get_weights_list(hole_cards, reverse=True)
        weights_statistic = self._statistic_weights(weights)
        weights_statistic_values = list(weights_statistic.values())
        if weights_statistic_values.count(2) == 2:
            return True
        else:
            return False

    def is_one_pair(self, hole_cards):
        """
        判断是否为一对
        """
        weights = self._get_weights_list(hole_cards, reverse=True)
        weights_statistic = self._statistic_weights(weights)
        if 2 in weights_statistic.values():
            return True
        else:
            return False

    def get_card_type(self, hole_cards):
        """
        判断一副牌的排型
        """
        if self.is_royal_flush(hole_cards):
            return 'Royal Flush'    # 0
        if self.is_straight_flush(hole_cards):
            return 'Straight Flush'
        if self.is_four_of_a_kind(hole_cards):
            return 'Four of a Kind'
        if self.is_fullhouse(hole_cards):
            return 'Fullhouse'
        if self.is_flush(hole_cards):
            return 'Flush'
        if self.is_straight(hole_cards):
            return 'Straight'
        if self.is_three_of_a_kind(hole_cards):
            return 'Three of a kind'
        if self.is_two_paires(hole_cards):
            return 'Two Pairs'
        if self.is_one_pair(hole_cards):
            return 'one Pair'
        else:
            return 'high card'

    def compare_hole_cards(self, cards1, cards2):
        """
        比较两组手牌
        return:
            cards1 > cards2:    1
            cards1 == cards2:   0
            cards1 < cards2:    -1
        """
        type1 = self.get_card_type(cards1)
        type2 = self.get_card_type(cards2)
        if self.CARD_TYPE.index(type1) < self.CARD_TYPE.index(type2):
            return -1
        elif self.CARD_TYPE.index(type1) > self.CARD_TYPE.index(type2):
            return 1
        # 同一种牌型的情况：
        if type1 == self.CARD_TYPE[0]:      # 同花大顺不分大小
            return 0


if __name__ == '__main__':
    tp = TexasPoker()
    hole_cards1 = tp.pop_hole_cards()
    hole_cards2 = tp.pop_hole_cards()
    flops = tp.pop_flop()
    turn = tp.pop_turn()
    rever = tp.pop_rever()
    merge_cards1 = tp.merge_cards(hole_cards1)
    merge_cards2 = tp.merge_cards(hole_cards2)
    print(merge_cards1)
    print(merge_cards2)
    c = tp.compare_hole_cards(hole_cards1, hole_cards2)
    print(c)
