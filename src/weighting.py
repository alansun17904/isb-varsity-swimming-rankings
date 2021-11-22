"""Alan Sun
Weighting function initialization, ISB Varsity Swim Rankings
11/21/2021

This module contains functionality that initializes the weighting function
based on the given parameters. The weighting functions avaliable can be
found in the white paper. Note that here, more weighting functions can be
added simply by modifying this class.
"""
import math


class Weight:
    def __init__(self, func_type, param, h_index):
        self.func_type = func_type
        self.param = param
        self.h_index = h_index

    def weighting(self, j):
        if j < 0:
            return 0
        try:
            return getattr(self, self.func_type)(j)
        except AttributeError:
            raise RuntimeError("The given weighting function is not a part of \
                    the support functions. Please initialize the program \
                    again with a valid weighting funtion hyperparameter.")

    def uniform(self, j):
        return self.param

    def linear(self, j):
        return max(0, (self.param - (j - 1)) / self.param)

    def polynomial(self, j):
        return ((11 - (j - 1)) ** self.param) / 11 ** self.param

    def exponential(self, j):
        return math.exp(-self.param * (j - 1))

    def sigmoidal(self, j):
        return 1 / (1 + math.exp(self.param * (j - self.h_index)))

