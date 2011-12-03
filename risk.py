import simulation
import mathmodel
import riskboard
import test_agent

def main():
    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    winners = {}
    for n in range(100):
        sim = simulation.Simulation(elist, model)
        sim.add_agent(test_agent.TestAgent())
        sim.add_agent(test_agent.TestAgent())
        sim.add_agent(test_agent.TestAgent())
        sim.add_agent(test_agent.TestAgent())
        sim.start()
        winner = sim.winner()
        print "Winner is %d" % winner
        winners[winner] = winners.get(winner, 0) + 1
    print winners
        

if __name__ == '__main__':
    main()
