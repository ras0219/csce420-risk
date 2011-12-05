import agent
from mathmodel import integral2d

class RedAgent(agent.Agent):
    def pregame_place(self, numarmies, sim):
        c = random.choice(sim.owns[self])
        return {c:numarmies}
