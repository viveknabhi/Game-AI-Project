import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 
from moba import *
from constants import *
from utils import *
from core import *
from itertools import combinations
import random

dims = (1200, 1200)

world = MOBAWorld(SEED, dims, dims, 1, 60)
agent = Hero((600, 500), 0, world, AGENT)
world.setPlayerAgent(agent)
agent.setNavigator(Navigator())
agent.team = 1
world.debugging = True

nav = AStarNavigator()

cellFactor = 3
cellsize = agent.getRadius()*2.0
bigCellsize = cellFactor*cellsize


def createBase(location):
	b1 = Base(BASE, location, world)
	#b1.setNavigator(nav)
	world.addBase(b1)

def getGameWorldObject(towerCount, baseCount, obstacleCount):
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


	gridPoints = [(x,y) for x in xlist for y in ylist]
	mainGridPoints = [(x2,y2) for x2 in x2list for y2 in y2list]

	for point in mainGridPoints:
		drawCross(world.debug, point)

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

getGameWorldObject(towerCount=6,baseCount=1,obstacleCount=3)
world.run()
