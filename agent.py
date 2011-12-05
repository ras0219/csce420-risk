class Agent:
    # set_id :: ID_TYPE -> IO ()
    def set_id(self, agent_id):
        # DO NOT OVERLOAD THIS
        self.agent_id = agent_id

    # preferred_ids :: [ID_TYPE]
    def preferred_ids(self, num):
        # This function returns a list of the agent's preferred names.
        # The simulation is under no obligation to follow this.
        return ["Super Agent #%02d" % num]

    # pregame_place :: Integer -> Simulation -> { String : Integer }
    def pregame_place(self, numarmies, sim):
        # Note on output format:
        #   Output should be a dictionary of countries to number of
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

    # __str__ :: String
    def __str__(self):
        # DO NOT OVERLOAD THIS
        return self.agent_id

    # __repr__ :: String
    def __repr__(self):
        # DO NOT OVERLOAD THIS
        return repr(str(self.agent_id))
