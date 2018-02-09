from nose.tools import assert_equal
from nose.tools import assert_raises
from nose.tools import assert_true
from nose.tools import assert_false


from texaspoker import TexasPoker


class TestTexasPoker:
    def setup(self):
        self.tp = TexasPoker()

    def test_if_straight(self):
        weights1 = [1, 2, 3, 4, 5, 7, 8]
        weights2 = [1, 2, 3, 4]
        weights3 = [1, 2, 3, 4, 6, 7]
        assert_true(self.tp._if_straight(weights1))
        assert_false(self.tp._if_straight(weights2))
        assert_false(self.tp._if_straight(weights3))

    def test_is_royal_flush(self):
        tp = TexasPoker()
        tp._flops = [['spade', 'A'], ['spade', 'J'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', 'K'], ['spade', '10']]
        assert_true(tp.is_royal_flush(hole_cards))

    def test_is_straight_flush(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['spade', 'J'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', 'K'], ['spade', '10']]
        assert_true(tp.is_straight_flush(hole_cards))
        tp._flops = [['spade', 'A'], ['spade', '4'], ['heart', 'A']]
        tp._turn = ['spade', '5']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', '2'], ['spade', '3']]
        assert_true(tp.is_straight_flush(hole_cards))

    def test_statistic_weights(self):
        tp = TexasPoker()
        weights = [10, 10, 8, 6, 3, 7, 7]
        statistics = tp._statistic_weights(weights)
        assert_equal(statistics[10], 2)
        assert_equal(statistics[8], 1)
        assert_equal(statistics[3], 1)
        assert_equal(statistics[6], 1)
        assert_equal(statistics[7], 2)

    def test_is_four_of_a_kind(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['spade', '9'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', '9'], ['spade', '9']]
        assert_true(tp.is_four_of_a_kind(hole_cards))

    def test_is_fullhouse(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['spade', '9'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', '9'], ['spade', 'K']]
        assert_true(tp.is_fullhouse(hole_cards))

    def test_is_flush(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['spade', 'K']
        hole_cards = [['spade', '8'], ['spade', 'K']]
        assert_true(tp.is_flush(hole_cards))

    def test_is_straight(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', '6']
        tp._rever = ['spade', '7']
        hole_cards = [['spade', '8'], ['spade', '10']]
        assert_true(tp.is_straight(hole_cards))

    def test_is_two_paires(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', '6']
        tp._rever = ['heart', '8']
        hole_cards = [['spade', '8'], ['spade', '10']]
        assert_true(tp.is_two_paires(hole_cards))

    def test_is_one_pair(self):
        tp = TexasPoker()
        tp._flops = [['spade', '3'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', '6']
        tp._rever = ['heart', '8']
        hole_cards = [['spade', '8'], ['spade', '10']]
        assert_true(tp.is_one_pair(hole_cards))

    def test_if_straight_return_largest(self):
        weights = [1, 2, 3, 4, 5, 9]
        tp = TexasPoker()
        assert_equal(5, tp._if_straight_return_largest(weights))

    def test_is_four_of_a_kind_weight(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['diamond', '9'], ['club', '9']]
        four_weight, single_weight = tp.is_four_of_a_kind_weight(hole_cards)
        assert_equal(8, four_weight)
        assert_equal(13, single_weight)

    def test_is_fullhouse_weights(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['heart', '9'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['diamond', '9'], ['spade', 'K']]
        three_weight, pair_weight = tp.is_fullhouse_weights(hole_cards)
        assert_equal(8, three_weight)
        assert_equal(12, pair_weight)

    def test_is_flush_weight(self):
        tp = TexasPoker()
        tp._flops = [['spade', '9'], ['spade', '3'], ['heart', 'A']]
        tp._turn = ['spade', 'Q']
        tp._rever = ['club', 'K']
        hole_cards = [['spade', '8'], ['spade', 'K']]
        assert_equal(12, tp.is_flush_weight(hole_cards))

    def test_if_straight_weight(self):
        weights1 = [1, 2, 3, 4, 5, 6, 9]
        weights3 = [1, 2, 3, 4, 5, 9]
        assert_equal(6, self.tp._if_straight_weight(weights1))
        assert_equal(5, self.tp._if_straight_weight(weights3))
