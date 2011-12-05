class RiskError(Exception):
    def __init__(self, agent, value):
        self.value = "[" + repr(str(agent)) + "]" + str(value)

    def __str__(self):
        return repr(self.value)
