class GraphSearch(object):
	def __init__(self, problem):
		self.problem = problem
		self.workspace = problem.workspace
		self.initial = problem.initial
		self.target = problem.target

	def graphSearch(self, criteria):
		frontier = [*self.problem.initial]
		explored = set()
		while True:
			if len(frontier):
				costsFrontier = list(map(criteria, frontier))
				path = frontier[costsFrontier.index(min(costsFrontier))]
				frontier.remove(path)

				s = path[-1]
				explored.add(s)

				if self.problem.goalTest(s):
					return path

				for a in self.problem.actions(s):
					result = self.problem.result(s, a)
					if result not in explored:
						frontier.append([*path, result])

			else:
				return False

	def breadthFirstSearch(self):
		return self.graphSearch(self.problem.pathCost)

	def aStar(self):
		return self.graphSearch(lambda x: self.problem.pathCost(x)+self.problem.heuristic(x[-1]))
