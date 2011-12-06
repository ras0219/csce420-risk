import simulation
import mathmodel
import riskboard
import test_agent
#import secret_agent
import red_agent
import red_agent_v2

def main():
    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    sglist = riskboard.region_memberships
    winners = {}

    for n in range(2,3):
        sim = simulation.Simulation(elist, sglist, model, False)
#        sim.add_agent(test_agent.TestAgent(0))
#        sim.add_agent(red_agent.RedAgent(minctw=0.5))
#        sim.add_agent(secret_agent.SecretAgent())
#        sim.add_agent(test_agent.TestAgent(1))
#        sim.add_agent(secret_agent.SecretAgent())
        sim.add_agent(red_agent_v2.RedAgent(minctw=0.9))
        sim.add_agent(red_agent.RedAgent(minctw=0.7))
        sim.add_agent(red_agent.RedAgent(minctw=0.7))
        sim.add_agent(red_agent_v2.RedAgent(minctw=0.7))

#        sim.set_logging("log%08d" % n)
        sim.set_logging("/home/rschumacher/public_html/BaronVsBaron%04d" % n)
        sim.start()
        winner = sim.winner()
        print "%3d) Winner is %s" % (n, winner)
        winners[str(winner)] = winners.get(str(winner), 0) + 1
        print winners
        

if __name__ == '__main__':
    main()
