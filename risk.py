#!/usr/bin/python

import simulation
import mathmodel
import riskboard
import test_agent
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option(
        "-l", "--logdir",
        action="store",
        dest="logdir",
        type="string", default=None,
        help="export images to logdir (use %d for round number)")
    parser.add_option(
        "-v", "--verbose",
        action="store_true", dest="verbose",
        default=False,
        help="enable verbose simulation output")
    parser.add_option(
        "-q", "--quiet",
        action="store_false", dest="verbose",
        help="disable verbose simulation output")
    parser.add_option(
        "-n", "--count",
        action="store", dest="count",
        type="int", default=1,
        help="specify number of rounds to run (default 1)")

    (options, args) = parser.parse_args()

    model = mathmodel.MathModel()
    elist = riskboard.territory_adjacency
    sglist = riskboard.region_memberships
    winners = {}

    for n in range(1,options.count+1):
        sim = simulation.Simulation(elist, sglist, model,
                                    debug=options.verbose)
        sim.add_agent(test_agent.TestAgent(0))
        sim.add_agent(test_agent.TestAgent(0))
        sim.add_agent(test_agent.TestAgent(1))
        sim.add_agent(test_agent.TestAgent(1))

        if options.logdir:
            try:
                ldir = options.logdir % n
            except TypeError:
                ldir = options.logdir
            sim.set_logging(ldir)
            sim.set_formats(['png'])
        sim.start()
        winner = sim.winner()
        print "%3d) Winner is %s" % (n, winner)
        winners[str(winner)] = winners.get(str(winner), 0) + 1
        print winners
        

if __name__ == '__main__':
    main()
