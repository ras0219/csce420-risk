class Agent:
    # set_id :: ID_TYPE -> IO ()
    def set_id(self, aid):
        self.aid = aid

    # pregame_place :: Integer -> Simulation -> { String : Integer }
    def pregame_place(self, numarmies, sim):
        # Note on output format:
        #   output should be a dictionary of countries to number of
        #   armies to place in said country
        #
        # IT IS LEGAL TO PLACE LESS THAN YOUR NUMBER OF ARMIES
        return {}

    # attack :: Simulation -> Maybe (String, String, Integer)
    def attack(self, sim):
        return None

    # transfer :: Simulation -> Maybe (String, String, Integer)
    def transfer(self, sim):
        return None

    # place_armies :: Integer -> Simulation -> { String : Integer }
    def place_armies(self, numarmies, sim):
        # See pregame_place for notes
        return {}
