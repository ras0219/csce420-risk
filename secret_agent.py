import agent
import random
import mathmodel

class SecretAgent(agent.Agent):
	def preferred_ids(self, num):
		return ["Secret Agent Man #%02d" % num]

	def pregame_place(self, numarmies, sim):
		c = random.choice(sim.owns[self.aid])
		return {c:numarmies}

	def attack(self, sim):
		self.sim = sim

		owned = sim.owns[self.aid]
		if len(owned) == 0:
			# Uh... we don't own anything...
			return None

		# Find the largest cluster of countries that we own
		stronghold = max(regions(owned, sim.edgelist), key=len)

		scorez = []
		for country in stronghold:
			# We don't have enough dudes to attack from this country
			# Retreat!!!!
			if self.army_size(country) < 2:
				break

			# Retrieve a list of neighboring countries
			neighbors = sim.edgelist[country]
			neighbors = filter(lambda c: sim.countries[c] != self.aid, neighbors)
			neighbors = sorted(neighbors, key=self.army_size)
			if len(neighbors) == 0:
				continue

			for neighbor in neighbors:
				#patch = sim.model.full_cdf()
				#chancetowin = mathmodel.integral2d(patch, lambda a1,a2: a1 > 0)
				# LOL there's a function for that LOL
				score = mathmodel.chance_to_win(neighbor.army_size, country)
				scorez += [(country, neighbor, score)]

		if(scorez):
			return sorted(scorez, key = lambda i: i[2]).pop()

		return None

	def place_armies(self, numarmies, sim):
		pregame_place(numarmies, sim)

	def army_size(self,c):
		return self.sim.armies[c]

