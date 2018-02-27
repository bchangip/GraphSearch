from PIL import Image
from numpy import*
from itertools import product
import time
import math
from graphSearch import GraphSearch


initial = []
target = []

discreteSquareSize = 30
inputImage = asarray(Image.open("input.jpg"))

# for j in inputImage:
#     new_temp = asarray([[i[0],i[1]] for i in j])

pixelSize = len(inputImage)

# print(pixelSize)

# for row in inputImage:
# 	for column in row:
# 		print(column)

intervals = list(range(0, pixelSize, discreteSquareSize))
if intervals[-1] != (pixelSize+1):
	intervals.append(pixelSize)

intervals = [range(intervals[i], intervals[i+1]) for i in range(len(intervals) - 1)]

discretizationMatrix = product(intervals, intervals)
# print(intervals)
# print(list(discretizationMatrix))

outputMatrix = [[0 for i in range(pixelSize)] for i in range(pixelSize)]
discreteMatrix = [[0 for i in range(len(intervals))] for i in range(len(intervals))]


for discreteSquare in discretizationMatrix:
	xs, ys = discreteSquare
	accumulatedR = 0
	accumulatedG = 0
	accumulatedB = 0

	for x in xs:
		for y in ys:
			accumulatedR += inputImage[y][x][0]
			accumulatedG += inputImage[y][x][1]
			accumulatedB += inputImage[y][x][2]

	avgR = accumulatedR / len(xs)**2
	avgG = accumulatedG / len(xs)**2
	avgB = accumulatedB / len(xs)**2


	# print("Square ", discreteSquare)
	# print(avgR)
	# print(avgG)
	# print(avgB)

	if(avgR < 100 and avgG < 100 and avgB < 100):
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "X"
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [0,0,0]
	elif(avgR > 150 and avgG < 50 and avgB < 50):
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "-"
		if(len(initial) == 0):
			initial.append([(int(xs[0]/discreteSquareSize),int(ys[0]/discreteSquareSize))])
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [255, 0, 0]
	elif(avgR < 50 and avgG > 150 and avgB < 50):
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "+"
		if(len(target) == 0):
			target.append((int(xs[0]/discreteSquareSize),int(ys[0]/discreteSquareSize)))
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [0, 255, 0]
	else:
		discreteMatrix[int(ys[0]/discreteSquareSize)][int(xs[0]/discreteSquareSize)] = "O"
		for x in xs:
			for y in ys:
				outputMatrix[y][x] = [255,255,255]


def actions(state):
	x, y = state
	posibleActions = []
	if(x+1 < len(discreteMatrix[0])):
		if(discreteMatrix[y][x+1] != 'X'):
			posibleActions.append("R")

	if(x-1 > 0):
		if(discreteMatrix[y][x-1] != 'X'):
			posibleActions.append("L")


	if(y+1 < len(discreteMatrix)):
		if(discreteMatrix[y+1][x] != 'X'):
			posibleActions.append("U")

	if(y-1 > 0):
		if(discreteMatrix[y-1][x] != 'X'):
			posibleActions.append("D")

	return posibleActions

def result(state, action):
	x, y = state
	if(action == 'R'):
		return (x+1,y)
	elif(action == 'L'):
		return (x-1,y)
	elif(action == 'U'):
		return (x,y+1)
	elif(action == 'D'):
		return (x,y-1)
	else:
		return state

def goalTest(state):
	x, y = state
	if(discreteMatrix[y][x] == '+'):
		return True
	else:
		return False

def stepCost(state, action):
	return 1

def pathCost(path):
	return len(path)-1

def heuristic(state):
	x, y = state
	targetX, targetY = target[0]
	return math.sqrt((targetX-x)**2 + (targetY-y)**2)

problem = {
	"workspace": discreteMatrix,
	"initial": initial,
	"target": target,
	"actions": actions,
	"result": result,
	"goalTest": goalTest,
	"stepCost": stepCost,
	"pathCost": pathCost,
	"heuristic": heuristic
}

graphSearch = GraphSearch(problem)
# # print(treeSearch.actions((3,3)))
# # print(treeSearch.goalTest((5,11)))
# start = time.time()
# resultBreadth = treeSearch.breadthFirstSearch()
# print("breadthFirstSearch time ", time.time()-start)
# if resultBreadth:
# 	for discreteSquare in resultBreadth[1:-1]:
# 		xDiscrete, yDiscrete = discreteSquare
# 		for x in range(xDiscrete*discreteSquareSize, (xDiscrete+1)*discreteSquareSize):
# 			for y in range(yDiscrete*discreteSquareSize, (yDiscrete+1)*discreteSquareSize):
# 				outputMatrix[y][x] = [0,0,255]


# 	import scipy.misc
# 	scipy.misc.imsave('outfileBreadth.jpg', outputMatrix)
# else:
# 	print("No solution was found")


start = time.time()
resultAStar = graphSearch.aStar()
print("aStar time ", time.time()-start)
if resultAStar:
	for discreteSquare in resultAStar[1:-1]:
		xDiscrete, yDiscrete = discreteSquare
		for x in range(xDiscrete*discreteSquareSize, (xDiscrete+1)*discreteSquareSize):
			for y in range(yDiscrete*discreteSquareSize, (yDiscrete+1)*discreteSquareSize):
				outputMatrix[y][x] = [0,0,255]


	import scipy.misc
	scipy.misc.imsave('outfileAStar.jpg', outputMatrix)
else:
	print("No solution was found")