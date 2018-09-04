from template import *

class TemplateSolver:
	def __init__(self, functions=Dict(), threshold=1, accuracy=1):
		self.threshold=threshold
		self.accuracy=accuracy
		self.functions=functions
		self.solutions=[]
		self.fitnesses=[]
		self.urgencies=[]
		self.problems=[]
		self.data = None
		self.result = None
		self.objective = None

	def __call__(self):
		output = Template()
		for i in self.result:
			if i in self.result:
				output.set(i, self.functions[i], FUNC)
		return output

	def update(self, data=None, objective=None):
		if data!=None and objective!=None:
			self.reset()
		if data==None:
			return self.result
		else:self.data=data
		if objective==None:
			objective=self.objective
		else:self.objective=objective
		if self.result==None:
			self.result=[]
			for i in range(len(objective)):
				self.result.append(UNKNOWN)
		self.problems=[]
		self.solutions=[]
		self.fitnesses=[]
		self.urgencies=[]
		for i in range(len(self.result)):
			if self.result[i]==UNKNOWN:
				self.problems.append(i)
				self.solutions.append([])
				self.fitnesses.append([])
				self.urgencies.append(0)
				for j in self.functions.keys():
					output=self.functions[j](self.data)
					target=self.objective[i]
					error=norm_error(output, target)
					fitness=logistic(-error)
					if fitness >= self.threshold:
						self.solutions[i].append(j)
						self.fitnesses[i].append(error)
						self.urgencies[i] += 1/len(self.functions)
		ordered=sort(self.urgencies)
		for i in ordered:
			utility = self.urgencies[i]
			functions = self.solutions[i]
			fitnesses = self.fitnesses[i]
			variable = self.problems[i]
			if len(fitnesses) > 0:
				ranked = sort(fitnesses)
				index=len(ranked)*self.accuracy
				if int(index)==0:index=0
				else:index=rr(int(index))
				keyword=functions[ranked[index]]
				solution=keyword
			else:solution=UNKNOWN
			self.result[variable]=solution
		return self.result
		
	def check(self):
		if self.result==None:
			return False
		if UNKNOWN in self.result:
			return False
		return True
	
	def reset(self):
		self.result=None
		self.objective=None
		self.data=None

