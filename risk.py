import simulation
import mathmodel
import riskboard
import test_agent

def main():
    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    winners = {}
    for n in range(50):
        sim = simulation.Simulation(elist, model)
        sim.add_agent(test_agent.TestAgent(0))
        sim.add_agent(test_agent.TestAgent(0))
        sim.add_agent(test_agent.TestAgent(1))
        sim.add_agent(test_agent.TestAgent(1))
        sim.start()
        winner = sim.winner()
        print "%3d) Winner is %s" % (n, winner)
        winners[str(winner)] = winners.get(str(winner), 0) + 1
    print winners
        

if __name__ == '__main__':
    main()
