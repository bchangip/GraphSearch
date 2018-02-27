class GraphSearch(object):
	def __init__(self, problem):
		self.workspace = problem["workspace"]
		self.initial = problem["initial"]
		self.target = problem["target"]
		self.actions = problem["actions"]
		self.result = problem["result"]
		self.goalTest = problem["goalTest"]
		self.stepCost = problem["stepCost"]
		self.pathCost = problem["pathCost"]
		self.heuristic = problem["heuristic"]

	def graphSearch(self, criteria):
		frontier = [*self.initial]
		explored = set()
		while True:
			if len(frontier):
				costsFrontier = list(map(criteria, frontier))
				path = frontier[costsFrontier.index(min(costsFrontier))]
				frontier.remove(path)

				s = path[-1]
				explored.add(s)

				if self.goalTest(s):
					return path

				for a in self.actions(s):
					result = self.result(s, a)
					if result not in explored:
						frontier.append([*path, result])

			else:
				return False

	def breadthFirstSearch(self):
		return self.graphSearch(len)

	def aStar(self):
		return self.graphSearch(lambda x: len(x)+self.heuristic(x[-1]))
