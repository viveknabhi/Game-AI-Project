import sys, pygame, math, random, time, copy
from pygame.locals import * 

from agents import *
from astarnavigator import *
from clonenav import *
from constants import *
from core import *
from moba import *
#from MyHero import *
from utils import *
from WanderingMinion import *

from itertools import combinations
import numpy as np

# dims = (1200, 1200)

# world = MOBAWorld(SEED, dims, dims, 0, 60)
# agent = Hero((600, 500), 0, world, AGENT)
# world.setPlayerAgent(agent)
# agent.setNavigator(Navigator())
# agent.team = 1
# world.debugging = True

# nav = AStarNavigator()


mapping = {'bases':1,'towers':2,'obstacles':0}

def generateMapRepresentation():
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

def createBase(image, position, world, team):#, minionType, heroType, buildrate = BUILDRATE, hitpoints = BASEHITPOINTS, firerate = BASEFIRERATE, bulletclass = BaseBullet):
	b = Base(image, position, world, team)#, minionType, heroType, buildrate, hitpoints, firerate, bulletclass)
	b.setNavigator(nav)
	world.addBase(b)

def createTower(location):
	t = Tower(TOWER, location, world, 2)
	world.addTower(t)

def createObstacle(x,y,size):
	val = cellFactor-1
	offset = bigCellsize/2 - cellsize
	topLeft = (x - offset, y - offset)
	topRight = (x + size*bigCellsize + offset, y - offset)
	bottomRight = (x + size*bigCellsize + offset, y + size*bigCellsize + offset)
	bottomLeft = (x - offset, y + size*bigCellsize + offset)

	obstacle = [topLeft, topRight, bottomRight, bottomLeft]
	return obstacle

def parseArrayRepresentation(A, x2list, y2list):
	obstacles = []

	gridPoints = [(x2,y2) for x2 in x2list for y2 in y2list]
	for i,x in enumerate(x2list):
		for j,y in enumerate(y2list):
			if A[i,j] == 0:
				obstacles.append(createObstacle(x,y,0))
			elif A[i,j] == 1:
				if i==0 and j==0:
					createBase(BASE, (x, y), world, 1)#, WanderingHumanMinion, MyHumanHero, BUILDRATE, 1000)
				else:
					createBase(BASE, (x,y), world, 2)#, WanderingAlienMinion, MyAlienHero, BUILDRATE, 1000)
			elif A[i,j] == 2:
				createTower((x,y))
	world.initializeTerrain(obstacles)

def getGridCoordinates():
	width, height = world.dimensions

	x = cellsize
	xlist = []
	while(x<width):
		xlist.append(x)
		x+=cellsize

	x2 = bigCellsize
	x2list = []
	while(x2<width):
		x2list.append(x2)
		x2+=bigCellsize

	y = cellsize
	ylist = []
	while(y<height):
		ylist.append(y)
		y+=cellsize

	y2 = bigCellsize
	y2list = []
	while(y2<height):
		y2list.append(y2)
		y2+=bigCellsize


	#gridPoints = [(x,y) for x in xlist for y in ylist]
	mainGridPoints = [(x2,y2) for x2 in x2list for y2 in y2list]
	print len(x2list), len(y2list)
	for point in mainGridPoints:
		drawCross(world.debug, point)
	
	return x2list, y2list

def getGameWorldObject(towerCount, baseCount, obstacleCount, x2list, y2list):

	obstacles = []
	count = 0
	while count<obstacleCount:
		obsX = random.choice(x2list[:-2])
		obsY = random.choice(y2list[:-2])

		val = cellFactor-1
		offset = bigCellsize/2 - cellsize
		topLeft = (obsX - offset, obsY - offset)
		topRight = (obsX + 2*bigCellsize + offset, obsY - offset)
		bottomRight = (obsX + 2*bigCellsize + offset, obsY + 2*bigCellsize + offset)
		bottomLeft = (obsX - offset, obsY + 2*bigCellsize + offset)

		obstacle = [topLeft, topRight, bottomRight, bottomLeft]
		inside = False
		for o in obstacles:
			for point in obstacle:
				if pointInsidePolygonPoints(point, o):
					inside = True
		if inside == False:
			obstacles.append(obstacle)
			count+=1

	world.initializeTerrain(obstacles)

	bases = []
	count = 0
	while count<baseCount:
		baseX = random.choice(x2list)
		baseY = random.choice(y2list)
		inside = False
		for o in obstacles:
			if pointInsidePolygonPoints((baseX, baseY), o):
				inside = True
		if inside == False:
			bases.append((baseX, baseY))
			x2list.remove(baseX)
			y2list.remove(baseY)
			count+=1
			b1 = Base(BASE, (baseX, baseY), world, 1)
			b1.setNavigator(nav)
			world.addBase(b1)


	towers = []
	count = 0
	while count<towerCount:
		towerX = random.choice(x2list)
		towerY = random.choice(y2list)
		inside = False
		for o in obstacles:
			if pointInsidePolygonPoints((towerX, towerY), o):
				inside = True
		if inside == False:
			towers.append((towerX, towerY))
			count+=1
			t11 = Tower(TOWER, (towerX, towerY), world, 1)
			world.addTower(t11)



############################
### SET UP WORLD

dims = (1200, 1200)

#obstacles = [[(250, 150), (600, 160), (590, 400), (260, 390)],
#			 [(800, 170), (1040, 140), (1050, 160), (1040, 500), (810, 310)]]


#mirror = map(lambda poly: map(lambda point: (dims[0]-point[0], dims[1]-point[1]), poly), obstacles)

#obstacles = obstacles + mirror

#obstacles = obstacles + [[(550, 570), (600, 550), (660, 570), (650, 630), (600, 650), (540, 630)]]



###########################
### Minion Subclasses
"""
class WanderingHumanMinion(WanderingMinion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		WanderingMinion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)

class WanderingAlienMinion(WanderingMinion):
	
	def __init__(self, position, orientation, world, image = JACKAL, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		WanderingMinion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)


########################
### Hero Subclasses

class MyHumanHero(class1):
	
	def __init__(self, position, orientation, world, image = AGENT, speed = SPEED, viewangle = 360, hitpoints = HEROHITPOINTS, firerate = FIRERATE, bulletclass = BigBullet, dodgerate = DODGERATE, areaeffectrate = AREAEFFECTRATE, areaeffectdamage = AREAEFFECTDAMAGE):
		class1.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass, dodgerate, areaeffectrate, areaeffectdamage)

class MyAlienHero(class2):
	
	def __init__(self, position, orientation, world, image = ELITE, speed = SPEED, viewangle = 360, hitpoints = HEROHITPOINTS, firerate = FIRERATE, bulletclass = BigBullet, dodgerate = DODGERATE, areaeffectrate = AREAEFFECTRATE, areaeffectdamage = AREAEFFECTDAMAGE):
		class2.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass, dodgerate, areaeffectrate, areaeffectdamage)
"""

########################

world = MOBAWorld(SEED, dims, dims, 0, 60)
#world = GameWorld(SEED, dims, dims)
agent = GhostAgent(AGENT, (600, 500), 1, SPEED, world)
world.setPlayerAgent(agent)

nav = AStarNavigator()
#nav.setWorld(world)

cellFactor = 3
cellsize = agent.getRadius()*2.0
bigCellsize = cellFactor*cellsize

#getGameWorldObject(towerCount=6, baseCount=1, obstacleCount=3, x2list, y2list)
x2list, y2list = getGridCoordinates()
A = generateMapRepresentation()
parseArrayRepresentation(A, x2list, y2list)
#world.initializeTerrain(obstacles, (0, 0, 0), 4)


agent.setNavigator(Navigator())
agent.team = 0
world.debugging = True


"""
b1 = Base(BASE, (25, 25), world, 1, WanderingHumanMinion, MyHumanHero, BUILDRATE, 1000)
b1.setNavigator(nav)
world.addBase(b1)

b2 = Base(BASE, (1075, 1075), world, 2, WanderingAlienMinion, MyAlienHero, BUILDRATE, 1000)
b2.setNavigator(nav)
world.addBase(b2)

hero1 = MyHumanHero((125, 125), 0, world)
hero1.setNavigator(cloneAStarNavigator(nav))
hero1.team = 1
world.addNPC(hero1)

hero2 = MyAlienHero((1025, 1025), 0, world)
hero2.setNavigator(cloneAStarNavigator(nav))
hero2.team = 2
world.addNPC(hero2)
"""
#world.makePotentialGates()


#hero1.start()
#hero2.start()

world.run()
