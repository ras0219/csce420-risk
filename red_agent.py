import agent
import graph_funcs
from mathmodel import integral2d
import random

class RedAgent(agent.Agent):
    def __init__(self):
        self.attack_iter = None
        self.domain = 0

    def preferred_ids(self, num):
        return ["The Red Baron","Senor Rojo","Floda Reltih","Darth Vader"]

    def pregame_place(self, numarmies, sim):
        return self.place_armies(numarmies, sim)

    def attack(self, sim):
        if self.attack_iter == None or self.domain < len(sim.owns[self]):
            self.attack_iter = self.attacking(sim)
        atk = next(self.attack_iter, None)
        if atk == None:
            self.attack_iter = None
            return None
        return atk

    def place_armies(self, numarmies, sim):
        regs = graph_funcs.regions(sim.owns[self], sim.edgelist)
        regs.sort(key=lambda cs: sum_armies(cs, sim))
        print "%s: %s" % (self, regs)
        raw_input()

        kernel = regs.pop()
        bord = graph_funcs.border(kernel, sim.edgelist)
        ibord = graph_funcs.inner_border(kernel, sim.edgelist)
        bstr = sum_armies(bord, sim)
        ibstr = sum_armies(ibord, sim)

        def country_value(c):
            kprime = [c]+kernel
            bprime = graph_funcs.border(kprime, sim.edgelist)
            ibprime = graph_funcs.inner_border(kprime, sim.edgelist)
            bstrprime = sum_armies(bprime, sim)
            army2 = sim.armies[c]
            neighs = filter(lambda k: sim.countries[k] == self, sim.edgelist[c])
            army1 = sum(map(lambda k: sim.armies[k]-1, neighs))
            p = sim.model.full_cdf(army1, army2)
            cost = integral2d(p, lambda a1,a2: army1-a1)

            return ((bstrprime - bstr) - cost)*(2**(len(ibord)-len(ibprime)))

        blist = [(country_value(c), c) for c in bord]
        blist.sort()
        print blist
        raw_input()
        targ = blist.pop()[1]
        for k in sim.edgelist[targ]:
            if sim.countries[k] == self:
                return {k:numarmies}

        # Should never get here, but just in case...
        return {regs[0]:numarmies}

    def attacking(self, sim):
        print "New Attacker Iter"
        regs = graph_funcs.regions(sim.owns[self], sim.edgelist)
        regs.sort(key=lambda cs: sum_armies(cs, sim))
        print "%s: %s" % (self, regs)
        raw_input()

        kernel = regs.pop()
        bord = graph_funcs.border(kernel, sim.edgelist)
        ibord = graph_funcs.inner_border(kernel, sim.edgelist)

        bstr = sum_armies(bord, sim)
        ibstr = sum_armies(ibord, sim)

        def country_value(c):
            kprime = [c]+kernel
            bprime = graph_funcs.border(kprime, sim.edgelist)
            ibprime = graph_funcs.inner_border(kprime, sim.edgelist)
            bstrprime = sum_armies(bprime, sim)
            army2 = sim.armies[c]
            neighs = filter(lambda k: sim.countries[k] == self, sim.edgelist[c])
            army1 = sum(map(lambda k: sim.armies[k]-1, neighs))
            p = sim.model.full_cdf(army1, army2)
            cost = integral2d(p, lambda a1,a2: army1-a1)
            return ((bstrprime - bstr) + (army1 - cost) / (army1 + 1)) \
                * (2**(len(ibord)-len(ibprime)))

        blist = [(country_value(c), c) for c in bord]
        blist.sort()
        print blist
        raw_input()

        self.domain = len(sim.owns[self])
        while self.domain == len(sim.owns[self]) and len(blist) > 0:
            tval,targ = blist.pop()
            if tval <= 0.5:
                print "Hit minimum tval: %s" % ((targ,tval),)
                raw_input()
                return
            army2 = sim.armies[targ]
            neighs = filter(lambda k: sim.countries[k] == self,
                            sim.edgelist[targ])
            army1 = sum(map(lambda k: sim.armies[k]-1, neighs))
            ctw = sim.model.chance_to_win(army1, army2)
            print "%3d %6f %s" % (army1, ctw, neighs)
            print "Chance to win against %s: %f" % (targ, ctw*100)
            while ctw > 0.6 and sim.countries[targ] != self:
                adj = filter(lambda k: sim.countries[k] == self,
                             sim.edgelist[targ])
                adj = sorted(adj,key=lambda k: sim.armies[k])
                print [(k,sim.armies[k]) for k in adj]

                src = adj.pop()
                yield (src, targ, sim.armies[src]-1)
                neighs = filter(lambda k: sim.countries[k] == self,
                                sim.edgelist[targ])
                army1 = sum(map(lambda k: sim.armies[k]-1, neighs))
                ctw = sim.model.chance_to_win(army1, army2)

def sum_armies(clist, sim):
    return sum(map(lambda c: sim.armies[c], clist))
