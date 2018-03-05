from abc import ABC, abstractmethod

class Problem(ABC):
	
	def __init__(self, workspace, initial, target):
		super().__init__()
		self.workspace = workspace
		self.initial = initial
		self.target = target

	@abstractmethod
	def actions(self, state):
		pass

	@abstractmethod
	def result(self, state, action):
		pass

	@abstractmethod
	def goalTest(self, state):
		pass

	@abstractmethod
	def stepCost(self, state, action):
		pass

	@abstractmethod
	def pathCost(self, path):
		pass

	@abstractmethod
	def heuristic(self, state):
		pass