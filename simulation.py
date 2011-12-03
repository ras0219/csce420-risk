import riskerror
import random

class Simulation:
    # data Simulation = Simulation Edgelist MathModel
    def __init__(self, elist, mmodel):
        self.edgelist = elist
        self.model = mmodel
        self.agent_id = 0
        self.agents = {}

    # add_agent :: Agent -> IO ()
    def add_agent(self, agent):
        agent.set_id(self.agent_id)
        self.agents[self.agent_id] = agent
        # Maybe change this to have agents be colors?
        self.agent_id += 1

    # start :: IO ()
    def start(self):
        # initialize map
        aids = self.agents.keys()
        num_agents = len(aids)
        self.countries = {}
        self.owns = {}
        self.armies = {}
        clist = self.edgelist.keys()
        random.shuffle(clist)
        for k in self.agents:
            self.owns[k] = []
        for c in range(len(clist)):
            aid = aids[c % num_agents]
            self.owns[aid].append(clist[c])
            self.countries[clist[c]] = aid
            self.armies[clist[c]] = 1

#        print "Countries"
#        print self.countries
#        print "Owns"
#        print self.owns
#        print "Armies"
#        print self.armies
        
        numarmies = self.model.pregame_armies
        for aid in self.agents:
            places = self.agents[aid].pregame_place(numarmies, self)
            self.process_placements(aid, numarmies, places)

        while not self.is_ended():
            # Begin game
            for aid in self.agents:
                if len(self.owns[aid]) == 0:
                    continue
                numarmies = self.model.num_armies(self.owns[aid])
                places = self.agents[aid].pregame_place(numarmies, self)
                self.process_placements(aid, numarmies, places)
                self.process_attacks(aid)
                self.process_transfers(aid)

#            print self.owns
#            print self.armies
            # Done with round

    def process_placements(self, aid, numarmies, places):
        if sum(places.values()) > numarmies:
            raise RiskError(aid, "Too many pregame self.armies")
        for p in places:
            if p not in self.countries:
                raise RiskError(aid, "Invalid Country "+repr(p))
            if not self.countries[p] == aid:
                raise RiskError(aid, "Unowned Country "+repr(p))
            if places[p] < 0:
                raise RiskError(aid, "Negative self.armies")
            self.armies[p] += places[p]
#        print "Agent "+str(aid)+" places self.armies:"
#        print places
#        print ""
        

    # process_transfers :: AgentID -> IO ()
    def process_attacks(self, aid):
        for mv in self.generate(self.agents[aid].attack):
            if mv[0] not in self.owns[aid]:
                raise RiskError(aid, "Unowned Source Country: "+repr(mv))
            if mv[1] in self.owns[aid]:
                raise RiskError(aid, "Owned Dest Country: "+repr(mv))
            if mv[2]+1 > self.armies[mv[0]]:
                raise RiskError(aid, "Too Many self.armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(aid, "Not Enough self.armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(aid, "Territories Not Adjacent: "+repr(mv))

            army1 = mv[2]
            army2 = self.armies[mv[1]]
            L1, L2 = self.model.perform_combat(army1, army2)
            self.armies[mv[1]] += L2
            if self.armies[mv[1]] > 0:
                self.armies[mv[0]] += L1
            else:
                # The attacker won
                self.transfer_ownership(mv[1], aid)
                self.armies[mv[0]] -= mv[2]
                self.armies[mv[1]] = mv[2] + L1
#            print "Agent "+str(aid)+" attacks:"
#            print mv
#            print "Results: %4s  vs %4s" % (army1,army2)
#            print "         %4s  vs %4s" % (L1, L2)
#            print ""

    # process_transfers :: AgentID -> IO ()
    def process_transfers(self, aid):
        activated = []
        for mv in self.generate(self.agents[aid].transfer):
            if mv[0] not in self.owns[aid]:
                raise RiskError(aid, "Unowned Source Country: "+repr(mv))
            if mv[1] not in self.owns[aid]:
                raise RiskError(aid, "Unowned Dest Country: "+repr(mv))
            if mv[2]+1 > self.armies[mv[0]]:
                raise RiskError(aid, "Too Many self.armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(aid, "Not Enough self.armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(aid, "Territories Not Adjacent: "+repr(mv))
            if mv[0] in activated:
                raise RiskError(aid,
                                "Cannot Move Into Activated Country: " +
                                repr(mv))
            self.armies[mv[0]] -= mv[2]
            self.armies[mv[1]] += mv[2]
            if mv[1] not in activated:
                activated.append(mv[1])
#            print "Agent "+str(aid)+" transfers:"
#            print mv
#            print ""

    # transfer_ownership :: String -> AgentID -> IO ()
    def transfer_ownership(self, land, agent):
        # Update all data structures needed to reflect change in ownership
        old = self.countries[land]
        self.owns[old].remove(land)
        self.owns[agent].append(land)
        self.countries[land] = agent

    # eval_turn :: (Simulation -> Move) -> Iterator Move
    def generate(self, agent_func):
        while True:
            mv = agent_func(self)
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
