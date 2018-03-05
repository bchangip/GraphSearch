from PIL import Image
from numpy import*
from itertools import product
import time
import math
from graphSearch import GraphSearch
from problem import Problem
from functools import lru_cache

initial = []
target = []

discreteSquareSize = 40
inputImage = asarray(Image.open("prueba.bmp"))

pixelSize = len(inputImage)

intervals = list(range(0, pixelSize, discreteSquareSize))
if intervals[-1] != (pixelSize+1):
	intervals.append(pixelSize)

intervals = [range(intervals[i], intervals[i+1]) for i in range(len(intervals) - 1)]

discretizationMatrix = product(intervals, intervals)

outputMatrix = [[0 for i in range(pixelSize)] for i in range(pixelSize)]
discreteMatrix = [[0 for i in range(len(intervals))] for i in range(len(intervals))]


for discreteSquare in discretizationMatrix:
	xs, ys = discreteSquare
	accumulatedR = 0
	accumulatedG = 0
	accumulatedB = 0

	colorsFound = set()

	for x in xs:
		for y in ys:
			r = inputImage[y][x][0]
			g = inputImage[y][x][1]
			b = inputImage[y][x][2]

			if(r > 150 and g < 50 and b < 50):
				colorsFound.add("R")
			elif(r < 50 and g > 150 and b < 50):
				colorsFound.add("G")
			elif(r < 50 and g < 50 and b < 50):
				colorsFound.add("B")
			else:
				colorsFound.add("W")

	if "G" in colorsFound:
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "+"
		target.append((int(xs[0]/discreteSquareSize),int(ys[0]/discreteSquareSize)))
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [0, 255, 0]
	elif "R" in colorsFound:
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "-"
		if(len(initial) == 0):
			initial.append([(int(xs[0]/discreteSquareSize),int(ys[0]/discreteSquareSize))])
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [255, 0, 0]
	elif "W" in colorsFound:
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "O"
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [255,255,255]
	else:
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "X"
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [0,0,0]

class ProblemDescription(Problem):
	def actions(self, state):
		x, y = state
		posibleActions = []
		if(x+1 < len(discreteMatrix[0])):
			if(discreteMatrix[y][x+1] != 'X'):
				posibleActions.append("R")

		if(x-1 >= 0):
			if(discreteMatrix[y][x-1] != 'X'):
				posibleActions.append("L")

		if(y-1 >= 0):
			if(discreteMatrix[y-1][x] != 'X'):
				posibleActions.append("U")

		if(y+1 < len(discreteMatrix)):
			if(discreteMatrix[y+1][x] != 'X'):
				posibleActions.append("D")

		return posibleActions

	def result(self, state, action):
		x, y = state
		if(action == 'R'):
			return (x+1,y)
		elif(action == 'L'):
			return (x-1,y)
		elif(action == 'U'):
			return (x,y-1)
		elif(action == 'D'):
			return (x,y+1)
		else:
			return state

	def goalTest(self, state):
		x, y = state
		if(discreteMatrix[y][x] == '+'):
			return True
		else:
			return False

	def stepCost(self, state, action):
		return 1

	def pathCost(self, path):
		return len(path)-1

	@lru_cache()
	def heuristic(self, state):
		x, y = state
		targetX, targetY = target[0]
		return min(map(
			lambda tgt: ((tgt[0]-x)**2 + (tgt[1]-y)**2)**0.5,
			target
		))


problemDescription = ProblemDescription(discreteMatrix, initial, target)
graphSearch = GraphSearch(problemDescription)


import scipy.misc
scipy.misc.imsave('outfileAStar.jpg', outputMatrix)
print("target", target)

start = time.time()
resultAStar = graphSearch.aStar()
print("aStar time ", time.time()-start)
if resultAStar:
	print("Solution found")
	for discreteSquare in resultAStar[1:-1]:
		xDiscrete, yDiscrete = discreteSquare
		for x in range(xDiscrete*discreteSquareSize, (xDiscrete+1)*discreteSquareSize):
			for y in range(yDiscrete*discreteSquareSize, (yDiscrete+1)*discreteSquareSize):
				if(y < len(outputMatrix) and x < len(outputMatrix[0])):
					outputMatrix[y][x] = [0,0,255]

else:
	print("No solution was found")

scipy.misc.imsave('outfileAStar.jpg', outputMatrix)