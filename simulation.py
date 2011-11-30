import riskerror
import random

class Simulation:
    PHASE_PREGAME = 0
    PHASE_PREPLACE = 1
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
        agents[agent_id] = agent
        agent_id++ # Maybe change this to have agents be colors?

    # start :: IO ()
    def start(self):
        while not is_ended():
            if phase == PHASE_PREGAME:
                # initialize map
                aids = agents.keys()
                num_agents = len(aids)
                self.countries = {}
                self.owns = {}
                clist = self.edgelist.keys()
                random.shuffle(clist)
                for k in agents:
                    self.owns[k] = []
                for c in range(len(clist)):
                    aid = aids[c % num_agents]
                    self.owns[aid].append(clist[c])
                    self.countries[clist[c]] = aid
                self.phase = PHASE_PREPLACE
            elif phase == PHASE_PREPLACE:
                numarmies = self.model.pregame_armies
                for aid in agents:
                    places = agents[aid].pregame_place(numarmies, self)
                    if sum(places.values()) > numarmies:
                        raise RiskError(str(aid)+" placed too many armies")
                    for p in places:
                        if 

            for aid in agents:
                eval_turn(aid)

    # eval_turn :: Agent -> IO ()
    def eval_turn(self, aid):

    # is_ended :: Bool
    def is_ended(self):
        # check win condition here
        return False
