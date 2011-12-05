import agent
import graph_funcs
from mathmodel import integral2d
import random

class RedAgent(agent.Agent):
    def __init__(self):
        self.attack_iter = None
        self.transfer_iter = None
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
        #print "%s: %s" % (self, regs)
        

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
            army1 = sum_armies(neighs, sim) - len(neighs)
            p = sim.model.full_cdf(army1, army2)
            ctw = integral2d(p, lambda a1,a2: army1-a1 > 0)
            cost = integral2d(p, lambda a1,a2: army1-a1)
            #return ((bstrprime - bstr) + (army1 - cost) / (army1 + 1)) \
            #    * (2**(len(ibord)-len(ibprime)))
            #return ((bstrprime-bstr-cost+(army1/army2/10.0))
            #        *ctw*(2**(len(ibord)-len(ibprime))))
            return ctw

        blist = [(country_value(c), c) for c in bord]
        blist.sort()
        #print blist
        
        targ = blist.pop()[1]
        for k in sim.edgelist[targ]:
            if sim.countries[k] == self:
                return {k:numarmies}

        # Should never get here, but just in case...
        return {regs[0]:numarmies}

    def attacking(self, sim):
        #print "New Attacker Iter"
        regs = graph_funcs.regions(sim.owns[self], sim.edgelist)
        regs.sort(key=lambda cs: sum_armies(cs, sim))
        #print "%s: %s" % (self, regs)
        

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
            army1 = sum_armies(neighs, sim) - len(neighs)
            p = sim.model.full_cdf(army1+1, army2)
            ctw = integral2d(p, lambda a1,a2: army1-a1 > 0)
            cost = integral2d(p, lambda a1,a2: army1-a1)
            #return ((bstrprime - bstr) + (army1 - cost) / (army1 + 1)) \
            #    * (2**(len(ibord)-len(ibprime)))
            #return ((bstrprime-bstr-cost+(army1/army2/10.0))
            #        *ctw*(2**(len(ibord)-len(ibprime))))
            return ctw

        blist = [(country_value(c), c) for c in bord]
        blist.sort()
        #print blist
        

        self.domain = len(sim.owns[self])
        while self.domain == len(sim.owns[self]) and len(blist) > 0:
            tval,targ = blist.pop()
            if tval <= 0:
                #print "Hit minimum tval: %s" % ((targ,tval),)
                return
            army2 = sim.armies[targ]
            neighs = filter(lambda k: sim.countries[k] == self,
                            sim.edgelist[targ])
            army1 = sum_armies(neighs, sim) - len(neighs)
            ctw = sim.model.chance_to_win(army1, army2)
            #print "%3d %6f %s" % (army1, ctw, neighs)
            #print "Chance to win against %s: %f" % (targ, ctw*100)
            while ctw > 0.5 and sim.countries[targ] != self:
                adj = filter(lambda k: sim.countries[k] == self,
                             sim.edgelist[targ])
                adj = sorted(adj,key=lambda k: sim.armies[k])
                #print [(k,sim.armies[k]) for k in adj]

                src = adj.pop()
                yield (src, targ, sim.armies[src]-1)
                neighs = filter(lambda k: sim.countries[k] == self,
                                sim.edgelist[targ])
                army1 = sum_armies(neighs, sim) - len(neighs)
                ctw = sim.model.chance_to_win(army1, army2)

    def transfer(self, sim):
        if self.transfer_iter == None:
            self.transfer_iter = self.transferring(sim)
        trns = next(self.transfer_iter, None)
        if trns == None:
            self.transfer_iter = None
            return None
        return trns

    def transferring(self, sim):
        regs = graph_funcs.regions(sim.owns[self], sim.edgelist)
        regs.sort(key=lambda cs: sum_armies(cs, sim))
        #print "%s: %s" % (self, regs)
        

        kernel = regs.pop()
        free_armies = sum_armies(kernel, sim) - len(kernel)
        bord = graph_funcs.border(kernel, sim.edgelist)
        ibord = graph_funcs.inner_border(kernel, sim.edgelist)
        bstr = sum_armies(bord, sim)
        ibstr = sum_armies(ibord, sim)

        def required_defenders(c):
            neighs = filter(lambda k: sim.countries[k] != self,
                            sim.edgelist[c])
            return max([1]+[sim.armies[k] for k in neighs])

        req_armies = sum([required_defenders(c) for c in kernel])

        slack = [(c,sim.armies[c] - required_defenders(c)) for c in kernel]
        slk = sorted(slack,key=lambda k: k[1],reverse=True)
        slack = dict(slk)
        #print slk

        while len(slk) > 0:
            c,p = slk.pop()
            srcs = filter(lambda k: k in slack and slack[k] > p, sim.edgelist[c])
            for src in srcs:
                if sim.armies[src] > 1:
                    yield (src, c, 1)

def sum_armies(clist, sim):
    return sum(map(lambda c: sim.armies[c], clist))
