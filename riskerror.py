class RiskError(Exception):
    def __init__(self, aid, value):
        self.value = "[" + repr(aid) + "]" + str(value)

    def __str__(self):
        return repr(self.value)
