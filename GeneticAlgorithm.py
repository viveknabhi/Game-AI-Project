from __future__ import division
from os import listdir
import numpy as np
import random
import time
from copy import deepcopy
import geneticHelper as GH
mapping = {'bases':1,'towers':2,'obstacles':0}

#Initilized constants
POP_SIZE = 50
GA_ITERATIONS = 100
MUTATION_RATE = 15
adjMat = []
trace_file_name = ''
elitism = True


#Class for each tour
class MapLayout:
	def __init__(s,mapRep):
		s.mapRep = mapRep
		#Modify to perform fitness function checks
		s.towers = s.findCount(2)
		s.obstacles = s.findCount(0)
		s.bases = s.findCount(1)
		s.cost = s.computeMapFitness()

	def findCount(s,item):
		return len([a for a in np.nditer(s.mapRep) if a == item])

	def computeMapFitness(s):
		score = s.towers * 5 + s.obstacles * 2
		return abs(score - 25)



	def getCost(s):
		return s.computeMapFitness(s.path)


#Class for a population a population has 50 MapLayout
class Population:
	def __init__(s,maxSize):
		s.listMapLayout = []
		s.maxSize = maxSize
		s.size = 0

	
	def generateMapRepresentation(s):
		#Generate a map with 100 free Spaces
		mapRep = np.empty((10,10))
		mapRep.fill(3)
		#Ensure first element of the map is always 1
		mapRep[0][0] = 1

		towerCount = random.randint(3,10)
		obsCount = random.randint(8,15)

		elements = {'bases':1,'towers':towerCount,'obstacles':obsCount}
		indices = list(np.ndindex(mapRep.shape))
		indices.pop(0)
		np.random.shuffle(indices)

		while len(elements) > 0:
			key = random.choice(elements.keys())
			elements[key] -= 1
			if elements[key] == 0:
				del elements[key]
			for index in indices:
				if mapRep[index[0]][index[1]] == 3:
					mapRep[index[0]][index[1]] = mapping[key]
					break

		return mapRep


	def createPopulation(s):
		i = 0
		while i < s.maxSize:
			i += 1
			mapRep = s.generateMapRepresentation()
			mapLayoutObj = MapLayout(mapRep)
			s.addTour(mapLayoutObj)
			s.size += 1

	def addTour(s,layout):
		if s.size +1 <= POP_SIZE:
			s.listMapLayout.append(layout)
			s.size += 1

	def getBestCost(s,localLayouts = None):
		minCost = float('inf')
		minPath = []
		if localLayouts == None:
			localLayouts = s.listMapLayout

		for layout in localLayouts:
			if layout.cost < minCost:
				minCost = layout.cost
				minPath = layout

		return minCost,minPath

	#Find the best crossover candidates based on tournament selection
	def getCrossoverCandidate(s):
		candidates = random.sample(s.listMapLayout,6)
		cost,layout = s.getBestCost(candidates)
		return layout



#Implementation of the Genetic Algorithm class
class GeneticAlgorithm:
	def __init__(s,mutationRate):
		s.p = Population(POP_SIZE)
		s.p.createPopulation()
		s.mutationRate = mutationRate

	def findGALayout(s,iters):
		i = 1
		t1 = time.time()
		cost,tour = s.p.getBestCost()
		print i,cost
		best = cost

		while i < iters:
			i += 1
			s.p = s.generateNewPopulation()
			print '******************** NEW population ****************************'	
			cost,tour = s.p.getBestCost()
			#t = time.time()-t1
			if cost < best:
				best = cost 
			print i,cost#,tour.path
		#print time.time() - t1
		return cost,tour

	#Generate a new population based on mutation and crossover
	def generateNewPopulation(s):
		offset = 0
		newP = Population(s.p.maxSize)
		if elitism:
			cost,tour = s.p.getBestCost()
			newP.addTour(tour)
			offset = 1
		i = offset
		while i < newP.maxSize:
			i += 1
			p1 = s.p.getCrossoverCandidate()
			p2 = s.p.getCrossoverCandidate()
			c1,c2 = s.crossover(p1,p2)
			c1 = s.mutate(c1)
			c2 = s.mutate(c2)
			mapLayoutObj1 = MapLayout(c1)
			mapLayoutObj2 = MapLayout(c2)
			newP.addTour(mapLayoutObj1)
			newP.addTour(mapLayoutObj2)

		return newP


	#Implementation of the 2-opt mutation
	def mutate(s,layout):

		choiceArr = set([0,2,3])
		for i in xrange(layout.shape[0]):
			for j in xrange(layout.shape[1]):
				if layout[i][j] == 1:
					continue

				if random.randint(1,100) < s.mutationRate:
					layout[i][j] = random.choice(list(choiceArr - set([layout[i][j]])))

		return layout


	#Generates 2 children by 1 point crossover
	def crossover(s,p1,p2):
		indices = list(np.ndindex(p1.mapRep.shape))
		child1 = np.empty((10,10))
		child1.fill(3)
		child2 = np.empty((10,10))
		child2.fill(3)
		crossCut = random.choice(indices)
		boolVar = True
		baseC1 = 2
		baseC2 = 2
		for i in xrange(p1.mapRep.shape[0]):
			for j in xrange(p1.mapRep.shape[1]):
				v1 = p1.mapRep[i][j]
				v2 = p2.mapRep[i][j]

				if boolVar:
					if v1 == 1:
						baseC1 -= 1
					if v2 == 1:
						baseC2 -= 1

					child1[i][j] = v1
					child2[i][j] = v2
				else:
					if v1 == 1:
						if baseC2 ==0:
							v1 = 3
						else:
							baseC2 -= 1

					if v2 == 1:
						if baseC1 == 0:
							v2 = 3
						else:
							baseC1 -= 1

					child1[i][j] = v2
					child2[i][j] = v1

		return child1,child2






def GA():

	cost = 0
	random.seed(20)
	np.random.seed(90)
	ga = GeneticAlgorithm(MUTATION_RATE)
	cost,layout = ga.findGALayout(GA_ITERATIONS)
	print layout,cost
	print layout.towers,layout.bases,layout.obstacles
	GH.generateMOBA(layout.mapRep)

GA()