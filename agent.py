class Agent:
    # set_id :: ID_TYPE -> IO ()
    def set_id(self, aid):
        self.aid = aid

    # pregame_place :: Integer -> Simulation -> { String : Integer }
    def pregame_place(self, numarmies, sim):
        return {}

    # attack :: Simulation -> Maybe (String, String, Integer)
    def attack(self, sim):
        return None

    # transfer :: Simulation -> Maybe (String, String, Integer)
    def transfer(self, sim):
        return None
