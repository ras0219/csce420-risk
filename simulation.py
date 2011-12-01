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
            for mv in generate(aid.attack):
                if mv[0] not in owns[aid]:
                    raise RiskError(aid, "Unowned Source Country "+repr(mv[0]))
                if mv[1] in owns[aid]:
                    raise RiskError(aid, "Owned Dest Country "+repr(mv[1]))
                if mv[2]+1 > armies[mv[0]]:
                    raise RiskError(aid, "Too many Armies")
                if mv[2] < 1:
                    raise RiskError(aid, "Not Enough Armies")

                self.model.perform_combat_round(
    # eval_turn :: Agent -> IO ()
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
