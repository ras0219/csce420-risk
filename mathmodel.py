# Premise of this file:
#
# The MathModel class should encapsulate all modifiable parameters
# and separate them from the core framework.  This is in pursuit of
# easy modification of core game rules (such as combat statistics)

import random

class MathModel:
    def __init__(self):
        self.pregame_armies = 10

    # num_armies :: [String] -> Integer
    def num_armies(self, country_list):
        # Inputs:
        #   country_list - a sequence of countries owned (Strings)
        # Output:
        #   number of armies earned
        #
        # TODO: implement proper algorithm for number of armies earned
        num = int(len(country_list)/3)
        if num < 3:
            num = 3
        return num

    # round_cdf :: Integer -> Integer -> {(Integer, Integer):Double}
    # army1 is the attacker, army2 is the defender
    # returns the dictionary:
    # {(newarmy1, newarmy2): <probability of that outcome>}
    def round_cdf(self, army1, army2):
        assert army1 >= 0, army2 >= 0

        # If army1 is too small to legitimately attack, return a convolution
        # pmf that has no effect
        if army1 < 1:
            return {(0,army2):1.00}

        # If army2 is too small to defend, return a convolution pmf that has no
        # effect
        if army2 < 1:
            return {(army1,0):1.00}

        
        if army1 == 1 and army2 == 1:
            return {(1,0):0.4167,
                    (0,1):0.5833}
        if army1 == 1 and army2 > 1:
            return {(1,army2-1):0.2546,
                    (0,army2):0.7454}
        if army1 == 2 and army2 == 1:
            return {(2,0):0.5787,
                    (1,1):0.4213}
        if army1 == 2 and army2 > 1:
            return {(2,army2-2):0.2276,
                    (1,army2-1):0.3241,
                    (0,army2):0.4483}
        if army1 > 2 and army2 == 1:
            return {(army1,0):0.6597,
                    (army1-1,1):0.3403}
        if army1 > 2 and army2 > 1:
            return {(army1,army2-2):0.3716,
                    (army1-1,army2-1):0.3358,
                    (army1-2,army2):0.2926}

        # False assertion to detect any gaps in the above logic
        assert False

    # full_cdf :: Integer -> Integer -> {(Integer, Integer):Double}
    def full_cdf(self, army1, army2):
        rounds = min((army1+1, army2+1))/2 + max((army1,army2))
        p = self.round_cdf(army1, army2)

        for r in range(rounds):
            p_new = {}
            for k,v in p.items():
                patch = self.round_cdf(*k)
                for k2,v2 in patch.items():
                    if v > 0 and v2 > 0:
                        p_new[k2] = p_new.get(k2, 0.00) + v*v2
            p = p_new
        return p

    # perform_combat :: Integer -> Integer -> (Integer, Integer)
    def perform_combat(self, army1, army2):
        r = random.random()
        cdf = self.round_cdf(army1, army2)
        for k,v in cdf.items():
            if v >= r:
                return k
            r -= v
        # The following should NEVER happen...
        return (0,0)

    def chance_to_win(self, army1, army2):
        p = self.full_cdf(army1, army2)
        c = integral2d(p, lambda a1,a2: a1 > 0)
        return c

    # minimum_defenders :: Integer -> Double -> Integer
    def minimum_defenders(self, army1, confidence):
        # Note: high confidence means high capture chance
        army2 = 1
        while True:
            if chance_to_win(army1, army2) <= confidence:
                return army2
            army2 += 1

    # minimum_attackers :: Integer -> Double -> Integer
    def minimum_attackers(self, army2, confidence):
        # Note: high confidence means high capture chance
        army1 = 1
        while True:
            if chance_to_win(army1, army2) >= confidence:
                return army1
            army1 += 1

# integral2d :: {(Integer, Integer):Double} -> (Integer -> Integer -> Double) -> Double
def integral2d(patch, util_func):
    acc = 0.0
    for k in patch:
        acc += patch[k] * util_func(*k)
    return acc
