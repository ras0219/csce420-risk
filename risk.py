import simulation
import mathmodel
import riskboard
import test_agent
import red_agent

def main():
    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    sglist = riskboard.region_memberships
    winners = {}

    for n in range(1):
        sim = simulation.Simulation(elist, sglist, model, debug=True)
        sim.add_agent(red_agent.RedAgent())
        sim.add_agent(test_agent.TestAgent(0))
        sim.add_agent(test_agent.TestAgent(1))
        sim.add_agent(test_agent.TestAgent(1))

        sim.set_logging("log%08d" % n)
        sim.start()
        winner = sim.winner()
        print "%3d) Winner is %s" % (n, winner)
        winners[str(winner)] = winners.get(str(winner), 0) + 1
        print winners
        

if __name__ == '__main__':
    main()
