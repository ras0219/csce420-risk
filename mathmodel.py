# Premise of this file:
#
# The MathModel class should encapsulate all modifiable parameters
# and separate them from the core framework.  This is in pursuit of
# easy modification of core game rules (such as combat statistics)

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

    # perform_combat :: Integer -> Integer -> Double -> (Integer, Integer)
    def perform_combat(self, army1, army2, rnd):
        # Inputs:
        #   army1 - size of player 1's army (Offense)
        #   army2 - size of player 2's army (Defense)
        #   rnd - randomness value
        # Outputs:
        #   L1 - L1 is losses to player 1
        #   L2 - L2 is losses to player 2
        #
        # TODO: Implement chance
        # Important note! It is ILLEGAL to return (army1,army2)
        #   unless both arguments were 0!
        #
        # Another important note:
        #   The passed in randomness value has limited amounts of randomness.
        #   This means that many combat outcomes are "inaccessible"
        #   To minimize this effect, and maximize AI compatibility, the combat
        #   function should be monotonically increasing with rnd.
        #
        #   This means that rnd=0 -> Offense wins, rnd=1.0 -> Defense wins!
        #   On the downside, this means extrapolating to additional bits of
        #   entropy is nontrivial.
        #
        #   Future modification may be required (pass in an integer with a
        #   set number of bits?)

        if army1 == army2 and army1 == 0:
            return (0,0)
        loss = min([army1, army2])
        if army1 == army2:
            return (loss, loss-1)
        return (loss, loss)
