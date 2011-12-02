import simulation
import mathmodel
import riskboard
import test_agent

def main():
    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    sim = simulation.Simulation(elist, model)
    sim.add_agent(test_agent.TestAgent())
    sim.add_agent(test_agent.TestAgent())
    sim.add_agent(test_agent.TestAgent())
    sim.add_agent(test_agent.TestAgent())
    sim.start()

if __name__ == '__main__':
    main()
