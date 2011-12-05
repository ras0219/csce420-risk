import agent
import random
import mathmodel
from itertools import ifilter

class RedAgent(agent.Agent):
    def __init__(self, minctw=0.7):
        self.minctw = minctw
        self.terraset = set()

    def preferred_ids(self, num):
        return ["Red Baron Returns", "Red Baron Returns (%d)" % num]

    def pregame_place(self, numarmies, sim):
        locs = sim.owns[self]
        adj_to_enemy = lambda c: len(filter(
                lambda k: sim.countries[k] != self,
                sim.edgelist[c]
                )
            ) > 0
        locs = filter(adj_to_enemy, locs)
        c = random.choice(locs)
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
            if chancetowin > self.minctw:
                return (src, dst, army1)
        return None

    def transfer(self, sim):
        owned = set(sim.owns[self])
        if self.terraset != owned:
            if sim.is_ended():
                return None
            # update radius graph
            self.tree = {}

            def on_current_edge(c):
                for k in sim.edgelist[c]:
                    if sim.countries[k] != self:
                        return True
                    if k in self.tree:
                        return True
                return False

            dist_to_edge = 0
            while len(owned) > 0:
                edges = filter(on_current_edge, owned)
                for e in edges:
                    self.tree[e] = dist_to_edge
                    owned.remove(e)
                dist_to_edge += 1
            self.terraset = set(sim.owns[self])
            self.unactivated = self.terraset.copy()
#            print self.tree

        owned = sorted(self.unactivated, key=lambda c: self.tree[c], reverse=True)
        while len(owned) > 0:
            c = owned.pop()
            if self.tree[c] == 0:
                continue
#            print owned, c
            if sim.armies[c] > 1:
                # find the gradient
                for k in sim.edgelist[c]:
                    if k in self.unactivated:
                        if self.tree[k] < self.tree[c]:
                            self.unactivated.remove(k)
                            return (c, k, sim.armies[c]-1)
        self.unactivated = self.terraset.copy()
        return None

    def place_armies(self, numarmies, sim):
        return self.pregame_place(numarmies, sim)

    def army_size(self,c):
        return self.sim.armies[c]

