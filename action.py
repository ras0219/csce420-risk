class Action:
    # The default action is to perform no action
    def __init__(self, aid):
        self.aid = aid

    def __str__(self):
        return "Null Action (Player "+str(self.aid)+")"

    def apply(self, sim):
        # this method should be overwritten to modify sim
        pass

