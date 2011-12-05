import agent
import random
import mathmodel

class TestAgent(agent.Agent):
    def pregame_place(self, numarmies, sim):
        c = random.choice(sim.owns[self])
        return {c:numarmies}

    def attack(self, sim):
        self.sim = sim
        # find territory we own with most units
        owned = sim.owns[self]
        if len(owned) == 0:
            # Uh... we don't own anything...
            return None
        top_owned = sorted(owned, key=self.army_size)

        while len(top_owned) > 0:
            src = top_owned.pop()
            if self.army_size(src) < 2:
                break
            neighbors = sim.edgelist[src]
            neighbors = filter(lambda c: sim.countries[c] != self, neighbors)
            neighbors = sorted(neighbors, key=self.army_size)
            if len(neighbors) == 0:
                continue
            dst = neighbors[0]
            army2 = self.army_size(dst)
            army1 = self.army_size(src) - 1

            patch = sim.model.full_cdf(army1, army2)
            chancetowin = mathmodel.integral2d(patch, lambda a1,a2: a1 > 0)
            if chancetowin > 0.7:
                return (src, dst, army1)
        return None

    def place_armies(self, numarmies, sim):
        return pregame_place(numarmies, sim)

    def army_size(self,c):
        return self.sim.armies[c]

