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
    def round_cdf(self, army1, army2):
        if army1 <= 0 or army2 <= 0:
            return {(0,0):1.00}
        if army1 == 1 and army2 == 1:
            return {(0,-1):0.4167,
                    (-1,0):0.5833}
        if army1 == 1 and army2 > 1:
            return {(0,-1):0.2546,
                    (-1,0):0.7454}
        if army1 == 2 and army2 == 1:
            return {(0,-1):0.5787,
                    (-1,0):0.4213}
        if army1 == 2 and army2 > 1:
            return {(0,-2):0.2276,
                    (-1,-1):0.3241,
                    (-2,0):0.4483}
        if army1 > 2 and army2 == 1:
            return {(0,-1):0.6597,
                    (-1,0):0.3403}
        return {(0,-2):0.3716,
                (-1,-1):0.3358,
                (-2,0):0.2926}

    # full_cdf :: Integer -> Integer -> {(Integer, Integer):Double}
    def full_cdf(self, army1, army2):
        rounds = min((army1+1, army2+1))/2 + max((army1,army2))
        p = self.round_cdf(0,0)

        for r in range(rounds):
            p_new = {}
            for k,v in p.items():
                patch = self.round_cdf(army1+k[0],army2+k[1])
                for k2,v2 in patch.items():
                    nk = (k[0]+k2[0], k[1]+k2[1])
                    if v > 0 and v2 > 0:
                        p_new[nk] = p_new.get(nk, 0.00) + v*v2
            p = p_new
        return p

    # perform_combat_round :: Integer -> Integer -> (Integer, Integer)
    def perform_combat(self, army1, army2):
        r = random.random()
        cdf = self.round_cdf(army1, army2)
        for k,v in cdf.items():
            if v >= r:
                return k
            r -= v
        # The following should NEVER happen...
        return (0,0)


# integral2d :: {(Integer, Integer):Double} -> ((Integer, Integer) -> Double) -> Double
def integral2d(patch, util_func):
    acc = 0.0
    for k in patch:
        acc += patch[k] * util_func(k)
    return acc
