import riskerror
import random

class Simulation:
    PHASE_PREGAME = 0
    PHASE_PLACE = 2
    PHASE_ATTACK = 3
    PHASE_TRANSFER = 4

    # data Simulation = Simulation Edgelist MathModel
    def __init__(self, elist, mmodel):
        self.edgelist = elist
        self.model = mmodel
        self.agent_id = 0
        self.phase = PHASE_PREGAME
        self.agents = {}

    # add_agent :: Agent -> IO ()
    def add_agent(self, agent):
        agent.set_id(agent_id)
        self.agents[agent_id] = agent
        # Maybe change this to have agents be colors?
        agent_id += 1

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

            numarmies = self.model.pregame_armies
            for aid in self.agents:
                places = self.agents[aid].pregame_place(numarmies, self)
                if sum(places.values()) > numarmies:
                    raise RiskError(aid, "Too many pregame armies")
                for p in places:
                    if p not in countries:
                        raise RiskError(aid, "Invalid Country "+repr(p))
                    if not countries[p] == aid:
                        raise RiskError(aid, "Unowned Country "+repr(p))
                    if places[p] < 0:
                        raise RiskError(aid, "Negative Armies")
                    self.armies[p] += places[p]

        # Begin game
        for aid in self.agents:
            self.process_attacks(aid)
            self.process_transfers(aid)

    # process_transfers :: AgentID -> IO ()
    def process_attacks(self, aid):
        for mv in generate(self.agents[aid].attack):
            if mv[0] not in owns[aid]:
                raise RiskError(aid, "Unowned Source Country: "+repr(mv))
            if mv[1] in owns[aid]:
                raise RiskError(aid, "Owned Dest Country: "+repr(mv))
            if mv[2]+1 > armies[mv[0]]:
                raise RiskError(aid, "Too Many Armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(aid, "Not Enough Armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(aid, "Territories Not Adjacent: "+repr(mv))
            L1, L2 = self.model.perform_combat(mv[2],
                                               armies[mv[1]],
                                               random.random())
            armies[mv[0]] -= mv[2]
            rem = mv[2] - L1
            armies[mv[2]] -= L2
            if rem > 0:
                # The attacker won
                transfer_ownership(mv[1], aid)
                armies[mv[1]] = rem

    # process_transfers :: AgentID -> IO ()
    def process_transfers(self, aid):
        activated = []
        for mv in generate(self.agents[aid].transfer):
            if mv[0] not in owns[aid]:
                raise RiskError(aid, "Unowned Source Country: "+repr(mv))
            if mv[1] not in owns[aid]:
                raise RiskError(aid, "Unowned Dest Country: "+repr(mv))
            if mv[2]+1 > armies[mv[0]]:
                raise RiskError(aid, "Too Many Armies: "+repr(mv))
            if mv[2] < 1:
                raise RiskError(aid, "Not Enough Armies: "+repr(mv))
            if mv[1] not in self.edgelist[mv[0]]:
                raise RiskError(aid, "Territories Not Adjacent: "+repr(mv))
            if mv[0] in activated:
                raise RiskError(aid,
                                "Cannot Move Into Activated Country: " +
                                repr(mv))
            armies[mv[0]] -= mv[2]
            armies[mv[1]] += mv[2]
            if mv[1] not in activated:
                activated.append(mv[1])

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
        # check win condition here
        return False
