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
from BaselineMinion import *

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

#module1 = __import__("BaselineMinion")
#class1 = getattr(module1, "BaselineMinion")

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

def generateMapRepresentationModified():
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
            	if key=='obstacles':
                	if index[0]+1<10 and mapRep[index[0]+1][index[1]]==3:
                		mapRep[index[0]+1][index[1]]=mapping[key]
                	if index[0]+1<10 and index[1]+1<10 and mapRep[index[0]+1][index[1]+1]==3:
                		mapRep[index[0]+1][index[1]+1]=mapping[key]
                	if index[1]+1<10 and mapRep[index[0]][index[1]+1]==3:
                		mapRep[index[0]][index[1]+1]=mapping[key]
                break

    return mapRep

def modifyMapObstacles(mapRep):
	for i in xrange(mapRep.shape[0]):
		for j in xrange(mapRep.shape[1]):
			if mapRep[i,j] == 0:
				if i+1<10 and mapRep[i+1][j]==3:
					mapRep[i+1][j]=0
				if i+1<10 and j+1<10 and mapRep[i+1][j+1]==3:
					mapRep[i+1][j+1]=0
				if j+1<10 and mapRep[i][j+1]==3:
					mapRep[i][j+1]=0
	return mapRep


###########################
### Minion Subclasses
#BaselineMinion
class MyHumanMinion(BaselineMinion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		BaselineMinion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)


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


class TweetMoba:
	def __init__(s):
		dims = (1200, 1200)
		s.world = MOBAWorld(SEED, dims, dims, 2, 60)
		#s.world = GameWorld(SEED, dims, dims)

		#s.agent = GhostAgent(AGENT, (600, 500), 1, SPEED, s.world)
		s.agentTemp = Hero((SCREEN[0]/2, SCREEN[1]/2), 0, s.world)

		s.cellFactor = 3
		s.cellsize = s.agentTemp.getRadius()*2.0
		s.bigCellsize = s.cellFactor*s.cellsize

		s.baseLocs = []
		s.towerLocs = []
		

	def createBase(s, position,fire):#, minionType, heroType, buildrate = BUILDRATE, hitpoints = BASEHITPOINTS, firerate = BASEFIRERATE, bulletclass = BaseBullet):
		if position == (25,25):
			b = Base(BASE, position, s.world, 1, MyHumanMinion, heroType = None,firerate = fire)
		else:
			b = Base(BASE, position, s.world, 3, heroType = None, minionType = None)#, minionType, heroType, buildrate, hitpoints, firerate, bulletclass)
		b.setNavigator(s.nav)
		s.world.addBase(b)

	def createTower(s, location,fire):
		t = Tower(TOWER, location, s.world, 2, firerate=fire)
		s.world.addTower(t)

	def createObstacle(s, x, y, size, i,j):
		offset = s.bigCellsize/2# - s.cellsize
		offset2 = s.bigCellsize/2 - s.cellsize

		if j==0:
			topLeft = (x - offset, y - offset2)
			topRight = (x + size*s.bigCellsize + offset, y - offset2)
		else:
			topLeft = (x - offset, y - offset)
			topRight = (x + size*s.bigCellsize + offset, y - offset)

		if i==9:
			topRight = (x + size*s.bigCellsize + offset2, y - offset)
			bottomRight = (x + size*s.bigCellsize + offset2, y + size*s.bigCellsize + offset)
		else:
			topRight = (x + size*s.bigCellsize + offset, y - offset)
			bottomRight = (x + size*s.bigCellsize + offset, y + size*s.bigCellsize + offset)

		if j==9:
			bottomRight = (x + size*s.bigCellsize + offset, y + size*s.bigCellsize + offset2)
			bottomLeft = (x - offset, y + size*s.bigCellsize + offset2)
		else:
			bottomRight = (x + size*s.bigCellsize + offset, y + size*s.bigCellsize + offset)
			bottomLeft = (x - offset, y + size*s.bigCellsize + offset)

		if i==0:
			topLeft = (x - offset2, y - offset)
			bottomLeft = (x - offset2, y + size*s.bigCellsize + offset)
		else:
			topLeft = (x - offset, y - offset)
			bottomLeft = (x - offset, y + size*s.bigCellsize + offset)

		obstacle = [topLeft, topRight, bottomRight, bottomLeft]
		return obstacle

	def parseArrayRepresentation(s, A, x2list, y2list):
		obstacles = []

		gridPoints = [(x2,y2) for x2 in x2list for y2 in y2list]
		for i in xrange(len(x2list)):
			for j in xrange(len(y2list)):
				if A[i,j] == 1:
					if j-1<10 and j-1>=0 and A[i,j-1]==0:
						A[i,j-1] = 3
					if i+1<10 and i+1>=0 and A[i+1,j]==0:
						A[i+1,j] = 3
					if j+1<10 and j+1>=0 and A[i,j+1]==0:
						A[i,j+1] = 3
					if i-1<10 and i-1>=0 and A[i-1,j]==0:
						A[i-1,j] = 3
					if j-1>=0 and i+1<10 and A[i+1,j-1]==0:
						A[i+1,j-1] = 3
					if i+1<10 and j+1<10 and A[i+1,j+1]==0:
						A[i+1,j+1] = 3
					if i-1>=0 and j+1<10 and A[i-1,j+1]==0:
						A[i-1,j+1] = 3
					if i-1>=0 and j-1>=0 and A[i-1,j-1]==0:
						A[i-1,j-1] = 3

		for i,x in enumerate(x2list):
			for j,y in enumerate(y2list):
				if A[i,j] == 0:
					obstacles.append(s.createObstacle(x,y,0,i,j))
				elif A[i,j] == 1:
					if i==0 and j==0:
						#s.createBase(BASE, (x, y), 1)#, WanderingHumanMinion, MyHumanHero, BUILDRATE, 1000)
						s.baseLocs.append((25,25))
					else:
						s.baseLocs.append((x,y))
						#s.createBase(BASE, (x,y), 2)#, WanderingAlienMinion, MyAlienHero, BUILDRATE, 1000)
				elif A[i,j] == 2:
					s.towerLocs.append((x,y))
					#s.createTower((x,y))
		s.world.initializeTerrain(obstacles,color=(255,255,255),sprite=TREE)

	def getGridCoordinates(s):
		width, height = s.world.dimensions

		x = s.cellsize
		xlist = []
		while(x<width):
			xlist.append(x)
			x+=s.cellsize

		x2 = s.bigCellsize
		x2list = []
		while(x2<width):
			x2list.append(x2)
			x2+=s.bigCellsize

		y = s.cellsize
		ylist = []
		while(y<height):
			ylist.append(y)
			y+=s.cellsize

		y2 = s.bigCellsize
		y2list = []
		while(y2<height):
			y2list.append(y2)
			y2+=s.bigCellsize


		#gridPoints = [(x,y) for x in xlist for y in ylist]
		mainGridPoints = [(x2,y2) for x2 in x2list for y2 in y2list]
		print len(x2list), len(y2list)
		for point in mainGridPoints:
			drawCross(s.world.debug, point)
		
		return x2list, y2list

	def getGameWorldObject(s, towerCount, baseCount, obstacleCount, x2list, y2list):

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

	def generateMOBA(s,A,fireRate):
		#getGameWorldObject(towerCount=6, baseCount=1, obstacleCount=3, x2list, y2list)
		x2list, y2list = s.getGridCoordinates()
		#A = generateMapRepresentation()
		s.parseArrayRepresentation(A, x2list, y2list)
		#world.initializeTerrain(obstacles, (0, 0, 0), 4)


		s.agent = Hero((125, 125), 0, s.world)
		s.agent.team = 1
		s.world.setPlayerAgent(s.agent)


		s.agent.setNavigator(Navigator())
		s.world.debugging = True


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
		s.world.makePotentialGates()

		s.nav = AStarNavigator()
		s.nav.setWorld(s.world)

		for location in s.baseLocs:
			s.createBase(location,fireRate)
		for location in s.towerLocs:
			s.createTower(location,fireRate)
		#hero1.start()
		#hero2.start()
		s.world.run()
