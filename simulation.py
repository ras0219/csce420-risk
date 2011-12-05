from riskerror import RiskError
from itertools import cycle
import random

class Simulation:
    # data Simulation = Simulation Edgelist MathModel
    def __init__(self, elist, mmodel, debug=False):
        self.edgelist = elist
        self.model = mmodel
        self.agents = []
        self.debug = debug

    # add_agent :: Agent -> IO ()
    def add_agent(self, a):
        prefnames = a.preferred_ids(len(self.agents))
        for name in prefnames:
            valid = True
            for agent in self.agents:
                if str(agent) == str(name):
                    valid = False
                    break
            if not valid:
                continue
            a.set_id(name)
            self.agents.append(a)
            return
        a.set_id("Default Agent #%02d" % len(self.agents))
        self.agents.append(a)

    # start :: IO ()
    def start(self):
        # initialize map
        self.countries = {}
        self.owns = {}
        self.armies = {}
        clist = self.edgelist.keys()
        random.shuffle(clist)
        for a in self.agents:
            self.owns[a] = []
        for c, a in zip(clist, cycle(self.agents)):
            self.owns[a].append(c)
            self.countries[c] = a
            self.armies[c] = 1

        if self.debug:
            print "Countries"
            print self.countries
            print "Owns"
            print self.owns
            print "Armies"
            print self.armies
        
        numarmies = self.model.pregame_armies
        for a in self.agents:
            places = a.pregame_place(numarmies, self)
            self.process_placements(a, numarmies, places)

        while not self.is_ended():
            # Begin game
            for a in self.agents:
                if len(self.owns[a]) == 0:
                    continue
                numarmies = self.model.num_armies(self.owns[a])
                places = a.place_armies(numarmies, self)
                self.process_placements(a, numarmies, places)
                self.process_attacks(a)
                self.process_transfers(a)
            if self.debug:
                print "------------"
                for agent in self.agents:
                    print "----%" % agent
                    print [(c, self.armies[c]) for c in self.owns[agent]]
                print "Armies: %d" % sum(
                    map(lambda c: self.armies[c], self.owns[agent]))
                print "Territories: %d" % len(self.owns[agent])
                print "------------"
            # Done with round

    def process_placements(self, a, numarmies, places):
        if sum(places.values()) > numarmies:
            raise RiskError(a, "Too many pregame self.armies")
        for p in places:
            if p not in self.countries:
                raise RiskError(a, "Invalid Country "+repr(p))
            if not self.countries[p] == a:
                raise RiskError(a, "Unowned Country "+repr(p))
            if places[p] < 0:
                raise RiskError(a, "Negative self.armies")
            self.armies[p] += places[p]
        if self.debug:
            print "%s places self.armies:" % a
            print places
            print ""
        

    # process_transfers :: Agent -> IO ()
    def process_attacks(self, a):
        for mv in self.generate(a.attack):
            if mv[0] not in self.owns[a]:
                raise RiskError(a, "Unowned Source Country: "+repr(mv))
            if mv[1] in self.owns[a]:
                raise RiskError(a, "Owned Dest Country: "+repr(mv))
            if mv[2]+1 > self.armies[mv[0]]:
                raise RiskError(a, "Too Many self.armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(a, "Not Enough self.armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(a, "Territories Not Adjacent: "+repr(mv))

            army1 = mv[2]
            army2 = self.armies[mv[1]]
            a1, a2 = self.model.perform_combat(army1, army2)
            self.armies[mv[0]] -= army1
            if a2 > 0:
                self.armies[mv[1]] = a2
                self.armies[mv[0]] += a1
            else:
                # The attacker won
                self.transfer_ownership(mv[1], a)
                self.armies[mv[1]] = a1
            if self.debug:
                print "%30s attacks: %s" % (a, mv)
                print "Results: %4s  vs %4s" % (army1, army2)
                print "    Now: %4s  vs %4s" % (a1, a2)
                print ""

    # process_transfers :: Agent -> IO ()
    def process_transfers(self, a):
        activated = []
        for mv in self.generate(a.transfer):
            if mv[0] not in self.owns[a]:
                raise RiskError(a, "Unowned Source Country: "+repr(mv))
            if mv[1] not in self.owns[a]:
                raise RiskError(a, "Unowned Dest Country: "+repr(mv))
            if mv[2]+1 > self.armies[mv[0]]:
                raise RiskError(a, "Too Many self.armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(a, "Not Enough self.armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(a, "Territories Not Adjacent: "+repr(mv))
            if mv[0] in activated:
                raise RiskError(a,
                                "Cannot Move Into Activated Country: " +
                                repr(mv))
            self.armies[mv[0]] -= mv[2]
            self.armies[mv[1]] += mv[2]
            if mv[1] not in activated:
                activated.append(mv[1])

            if self.debug:
                print "%s transfers:" % a
                print mv
                print ""

    # transfer_ownership :: String -> A -> IO ()
    def transfer_ownership(self, land, a):
        # Update all data structures needed to reflect change in ownership
        old = self.countries[land]
        self.owns[old].remove(land)
        self.owns[a].append(land)
        self.countries[land] = a

    # eval_turn :: (Simulation -> Move) -> Iterator Move
    def generate(self, a_func):
        while True:
            mv = a_func(self)
            if mv == None:
                break
            yield mv

    # is_ended :: Bool
    def is_ended(self):
        rem_players = 0
        # check win condition here
        for k,v in self.owns.items():
            if len(v) > 0:
                rem_players += 1
        return rem_players <= 1

    def winner(self):
        for k,v in self.owns.items():
            if len(v) > 0:
                return k
        return None
