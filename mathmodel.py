class MathModel:
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

    # perform_combat_round :: Integer -> Integer -> (Integer, Integer)
    def perform_combat_round(self, army1, army2):
        # Inputs:
        #   army1 - size of player 1's army
        #   army2 - size of player 2's army
        # Outputs:
        #   L1 - L1 is losses to player 1
        #   L2 - L2 is losses to player 2
        #
        # TODO: Implement chance
        loss = min([army1, army2])
        return (loss, loss)
