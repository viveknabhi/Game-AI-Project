from __future__ import division
from os import listdir
import numpy as np
import random
import time
from copy import deepcopy
#import geneticHelper as GH
from geneticHelper import *
from utils import *

mapping = {'bases':1,'towers':2,'obstacles':0}

#Initilized constants
POP_SIZE = 50
GA_ITERATIONS = 20
MUTATION_RATE = 5
adjMat = []
trace_file_name = ''
elitism = True

MIN_TOWER = 3
MAX_TOWER = 12

MIN_OBSTACLE = 15
MAX_OBSTACLE = 25

MIN_FIRE_RATE = 10
MAX_FIRE_RATE = 30
DELTA_FIRE_RATE = 0.5


#Class for each tour
class MapLayout:
	def __init__(s,mapRep,level,sentiment,baseFireRate):
		s.mapRep = mapRep
		#Modify to perform fitness function checks
		s.towers = s.findCount(2)
		s.obstacles = s.findCount(0)
		s.bases = s.findCount(1)
		s.sentiment = sentiment
		s.level = level

		s.baseFireRate = baseFireRate

		s.towerIndices = s.findItems(2)
		s.baseIndices = s.findItems(1)
		#print s.baseIndices


		s.TOWER_WEIGHT = 15
		s.OBSTACLE_WEIGHT = 2
		s.BASE_TOWER_DIST_WEIGHT = 15
		s.HBASE_TOWER_DIST_WEIGHT = 5
		s.BASE_BASE_DIST_WEIGHT = 20
		s.FIRE_RATE_WEIGHT = 5

		s.TOTAL_WEIGHT = s.TOWER_WEIGHT + s.OBSTACLE_WEIGHT + s.BASE_TOWER_DIST_WEIGHT + s.BASE_BASE_DIST_WEIGHT + s.HBASE_TOWER_DIST_WEIGHT  + s.FIRE_RATE_WEIGHT

		s.RANGE = int(s.TOTAL_WEIGHT/4)
		s.MIN =  s.RANGE * s.level
		s.MAX = s.MIN + s.RANGE

		s.targetScore = (s.MAX+s.MIN)/2
		#print s.targetScore

		try:
			assert s.bases == 2
			assert s.towers <= MAX_TOWER
			assert s.obstacles <= MAX_OBSTACLE 
		except:
			print s.bases,s.towers,s.obstacles
			print mapRep
			raw_input()
		#s.baseIndices.remove((0,0))

		s.cost = s.computeMapFitness()

	def findItems(s,item):
		rows,cols = np.where(s.mapRep == item)
		result = []
		for i in zip(rows,cols):
			result.append(i)

		return result

	def findCount(s,item):
		return len([a for a in np.nditer(s.mapRep) if a == item])

	def computeMapFitness(s):

		score = 0
		score += (s.towers/MAX_TOWER) * s.TOWER_WEIGHT
		score += (s.obstacles/MAX_OBSTACLE) * s.OBSTACLE_WEIGHT

		groupDistance = 0.1
		for base in s.baseIndices:
			if base == (0,0):
				continue

			for tower in s.towerIndices:
				groupDistance += distance(base,tower)

		score += (1/groupDistance) * s.BASE_TOWER_DIST_WEIGHT

		groupDistance = 0.1
		for base in s.baseIndices:
			if base != (0,0):
				continue

			for tower in s.towerIndices:
				groupDistance += distance(base,tower)

		score += (groupDistance/(distance((9,9),(1,1)) * 10)) * s.HBASE_TOWER_DIST_WEIGHT	
		score +=(distance(s.baseIndices[0],s.baseIndices[1])/(distance((9,9),(1,1)) * 10)) * s.BASE_BASE_DIST_WEIGHT

		baseFireScore = 0
		localFire = (s.baseFireRate - MIN_FIRE_RATE)/(MAX_FIRE_RATE- MIN_FIRE_RATE)
		baseFireScore = abs(s.sentiment-localFire) * s.FIRE_RATE_WEIGHT

		score += baseFireScore

		print s.targetScore,score

		return abs(score - s.targetScore)



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

		towerCount = random.randint(MIN_TOWER,MAX_TOWER)
		obsCount = random.randint(MIN_OBSTACLE,MAX_OBSTACLE)

		elements = {'bases':1,'towers':towerCount,'obstacles':obsCount}
		indices = list(np.ndindex(mapRep.shape))
		indices.pop(0)
		np.random.shuffle(indices)

		while len(elements) > 0:
			key = random.choice(elements.keys())
			elements[key] -= 1
			# print elements
			# print key
			# raw_input()
			if elements[key] == 0:
				del elements[key]
			for index in indices:
				if mapRep[index[0]][index[1]] == 3:
					mapRep[index[0]][index[1]] = mapping[key]
					break

		if 'bases' in elements:
			i,j = random.choice(indices)
			mapRep[i][j] = 1


		return mapRep

	def generateMapRepresentationModified(s):
		#Generate a map with 100 free Spaces
		mapRep = np.empty((10,10))
		mapRep.fill(3)
		#Ensure first element of the map is always 1
		mapRep[0][0] = 1

		towerCount = random.randint(MIN_TOWER,MAX_TOWER)
		obsCount = random.randint(MIN_OBSTACLE,MAX_OBSTACLE)

		elements = {'bases':1,'towers':towerCount,'obstacles':obsCount}
		indices = list(np.ndindex(mapRep.shape))
		indices.pop(0)
		np.random.shuffle(indices)

		while len(elements) > 0:
			key = random.choice(elements.keys())
			elements[key] -= 1
			if elements[key] <= 0:
				del elements[key]
			for index in indices:
				if mapRep[index[0]][index[1]] == 3:
					mapRep[index[0]][index[1]] = mapping[key]
					if key=='obstacles' and key in elements:
						if index[0]+1<10 and mapRep[index[0]+1][index[1]]==3 and elements[key] > 0:
							mapRep[index[0]+1][index[1]]=mapping[key]
							elements[key] -= 1
						if index[0]+1<10 and index[1]+1<10 and mapRep[index[0]+1][index[1]+1]==3  and elements[key] > 0:
							mapRep[index[0]+1][index[1]+1]=mapping[key]
							elements[key] -= 1
						if index[1]+1<10 and mapRep[index[0]][index[1]+1]==3  and elements[key] > 0:
							mapRep[index[0]][index[1]+1]=mapping[key]
							elements[key] -= 1

						if elements[key] <= 0:
							del elements[key]							
					break

		if 'bases' in elements:
			i,j = random.choice(indices)
			mapRep[i][j] = 1

		return mapRep

	def createPopulation(s,level,sentiment):
		i = 0
		while i < s.maxSize:
			i += 1
			#mapRep = s.generateMapRepresentation()
			baseFireRate = random.randint(MIN_FIRE_RATE,MAX_FIRE_RATE)

			mapRep = s.generateMapRepresentationModified()
			mapLayoutObj = MapLayout(mapRep,level,sentiment,baseFireRate)

			

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
		cost,tour = s.getBestCost(candidates)
		return tour



#Implementation of the Genetic Algorithm class
class GeneticAlgorithm:
	def __init__(s,mutationRate,level,sentiment):
		s.p = Population(POP_SIZE)
		s.p.createPopulation(level,sentiment)
		s.mutationRate = mutationRate
		s.level = level
		s.sentiment = sentiment

	def findGALayout(s,iters):
		i = 1
		t1 = time.time()
		cost,tou = s.p.getBestCost()
		print i,cost
		best = cost

		while i < iters:
			i += 1
			s.p = s.generateNewPopulation()
			print '******************** NEW population '+ str(i) +' ****************************'	
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
			c1,c2,c1Dict,c2Dict,bfr1,bfr2 = s.crossover(p1,p2)

			c1,bfr1 = s.mutate(c1,c1Dict,bfr1)
			c2,bfr2 = s.mutate(c2,c2Dict,bfr2)

			mapLayoutObj1 = MapLayout(c1,s.level,s.sentiment,bfr1)
			mapLayoutObj2 = MapLayout(c2,s.level,s.sentiment,bfr2)
			newP.addTour(mapLayoutObj1)
			#print i
			newP.addTour(mapLayoutObj2)

		return newP


	#Implementation of the 2-opt mutation
	def mutate(s,layout,cDict,bfr):
		choiceArr = set([0,2,3])
		if random.randint(1,100) < s.mutationRate:
			if random.choice([0,1]) == 0:
				bfr -= DELTA_FIRE_RATE
			else:
				bfr += DELTA_FIRE_RATE

			if bfr > MAX_FIRE_RATE:
				bfr = MAX_FIRE_RATE
			elif bfr < MIN_FIRE_RATE:
				bfr = MIN_FIRE_RATE


		for i in xrange(layout.shape[0]):
			for j in xrange(layout.shape[1]):
				if layout[i][j] == 1:
					continue

				if random.randint(1,100) < s.mutationRate:
					choice = random.choice(list(choiceArr - set([layout[i][j]])))

					if choice in cDict:
						if cDict[choice] > 0:
							cDict[choice] -= 1
						else:
							continue

					replaced = layout[i][j]
					if replaced in cDict:
						cDict[replaced] += 1

					layout[i][j] = choice

		return layout,bfr

	def checkUpperBounds(s,countDict,val):
		if val == 3:
			return 3

		if countDict[val] == 0:
			return 3
		elif countDict[val] > 0:
			countDict[val] -= 1
			return val


	#Generates 2 children by 1 point crossover
	def crossover(s,p1,p2):
		
		indices = list(np.ndindex(p1.mapRep.shape))
		indices.pop(0)
		child1 = np.empty((10,10))
		child1.fill(3)
		child2 = np.empty((10,10))
		child2.fill(3)

		child1[0][0] = 1
		child2[0][0] = 1

		#print p1.baseIndices,p2.baseIndices
		enemyBases = [x for x in p1.baseIndices if x != (0,0)] + [x for x in p2.baseIndices if x != (0,0)]
		#print enemyBases

		c1Dict = {0:MAX_OBSTACLE,1:1,2:MAX_TOWER}
		c2Dict = {0:MAX_OBSTACLE,1:1,2:MAX_TOWER}

		#uniform crossover
		length = len(indices)
		np.random.shuffle(indices)
		upper = indices[:int(length/2)]
		lower = indices[int(length/2):]

		for i,j in upper:
			v1 = s.checkUpperBounds(c1Dict,p1.mapRep[i][j])
			v2 = s.checkUpperBounds(c2Dict,p2.mapRep[i][j])


			# print c1Dict
			# print p1.mapRep[i][j]
			# raw_input()

			child1[i][j] = v1
			child2[i][j] = v2

		for i,j in lower:
			v1 = s.checkUpperBounds(c2Dict,p1.mapRep[i][j])
			v2 = s.checkUpperBounds(c1Dict,p2.mapRep[i][j])

			# print c1Dict
			# print p2.mapRep[i][j]
			# raw_input()

			child1[i][j] = v2
			child2[i][j] = v1

		#1-point crossover
		
		# crossCut = random.choice(indices)
		# boolVar = True
		# for i,j in indices:
		# 		if boolVar:
		# 			v1 = s.checkUpperBounds(c1Dict,p1.mapRep[i][j])
		# 			v2 = s.checkUpperBounds(c2Dict,p2.mapRep[i][j])
		# 			child1[i][j] = v1
		# 			child2[i][j] = v2
		# 		else:
		# 			v1 = s.checkUpperBounds(c2Dict,p1.mapRep[i][j])
		# 			v2 = s.checkUpperBounds(c1Dict,p2.mapRep[i][j])
		# 			child1[i][j] = v2
		# 			child2[i][j] = v1
		

		#Check if both children have 2 bases
		if c1Dict[1] == 1:
			i,j = random.choice(enemyBases)
			child1[i][j] = 1
			c1Dict[1] -= 1

		if c2Dict[1] == 1:
			i,j = random.choice(enemyBases)
			child2[i][j] = 1
			c2Dict[1] -= 1

		#print c1Dict,c2Dict
		bfr1 = p1.baseFireRate
		bfr2 = p2.baseFireRate
		ch = random.choice([1,2])
		if ch == 2:
			bfr1 = p2.baseFireRate
			bfr2 = p1.baseFireRate

		return child1,child2,c1Dict,c2Dict,bfr1,bfr2


def GA(level,sentiment):
	cost = 0
	seed = random.randint(0,100)
	random.seed(seed)
	np.random.seed(seed)
	ga = GeneticAlgorithm(MUTATION_RATE,level,sentiment)
	cost,layout = ga.findGALayout(GA_ITERATIONS)
	
	print layout.baseFireRate
	# print layout,cost
	# print layout.towers,layout.bases,layout.obstacles
	#layout.mapRep = GH.modifyMapObstacles(layout.mapRep)
	moba = TweetMoba()
	moba.generateMOBA(layout.mapRep,layout.baseFireRate)