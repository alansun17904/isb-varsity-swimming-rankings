from math import exp
from src.weighting import Weight

class TestWeight:
    def test_linear(self):
        w = Weight("linear", 11, 6)
        assert w.weighting(20) == 0
        assert w.weighting(-20) == 0
        assert w.weighting(1) == 1
        assert w.weighting(2) == 10 / 11
        assert w.weighting(3) == 9 / 11
        assert w.weighting(4) == 8 / 11
        assert w.weighting(5) == 7 / 11
        assert w.weighting(6) == 6 / 11
        assert w.weighting(7) == 5 / 11
        assert w.weighting(8) == 4 / 11
        assert w.weighting(9) == 3 / 11
        assert w.weighting(10) == 2 / 11

    def test_uniform(self):
        w = Weight("uniform", 1, 20)
        for i in range(1, 100):
            assert w.weighting(i) == 1

    def test_polynomial(self):
        w = Weight("polynomial", 2, 6)
        assert w.weighting(1) == 1
        assert w.weighting(2) == 100 / 121
        assert w.weighting(3) == 81 / 121
        assert w.weighting(4) == 64 / 121
        assert w.weighting(5) == 49 / 121
        assert w.weighting(6) == 36 / 121
        assert w.weighting(7) == 25 / 121
        assert w.weighting(8) == 16 / 121
        assert w.weighting(9) == 9 / 121
        assert w.weighting(10) == 4 / 121

