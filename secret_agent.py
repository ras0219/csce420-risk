import agent
import random
import mathmodel
import graph_funcs

class SecretAgent(agent.Agent):
	def __init__(self):
		self.mm = mathmodel.MathModel()

	def preferred_ids(self, num):
		return ["Secret Agent Man #%02d" % num]

	def pregame_place(self, numarmies, sim):
		c = random.choice(sim.owns[self])
		return {c:numarmies}

	def attack(self, sim):
		self.sim = sim

		owned = sim.owns[self]
		if len(owned) == 0:
			# Uh... we don't own anything...
			return None

		# Find the largest cluster of countries that we own
		stronghold = max(graph_funcs.regions(owned, sim.edgelist), key=len)

		scorez = []
		for country in stronghold:
			# We don't have enough dudes to attack from this country
			# Retreat!!!!
			if self.army_size(country) < 2:
				break

			# Retrieve a list of neighboring countries
			neighbors = sim.edgelist[country]
			neighbors = filter(lambda c: sim.countries[c] != self, neighbors)
			neighbors = sorted(neighbors, key=lambda i: sim.armies[i])
			if len(neighbors) == 0:
				continue

			for neighbor in neighbors:
				#patch = sim.model.full_cdf()
				#chancetowin = mathmodel.integral2d(patch, lambda a1,a2: a1 > 0)
				# LOL there's a function for that LOL
				score = self.mm.chance_to_win(sim.armies[neighbor], sim.armies[country])
				scorez += [(country, neighbor, score)]

		if(scorez):
			return sorted(scorez, key = lambda i: i[2]).pop()

		return None

	def place_armies(self, numarmies, sim):
		return self.pregame_place(numarmies, sim)

	def army_size(self,c):
		return self.sim.armies[c]

