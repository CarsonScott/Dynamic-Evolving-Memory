from template import *

class Pool(Template):
	def __init__(self, capocity, data=[], selection=rand_select):
		self.assign('size', len(data))
		self.assign('capacity', capacity)
		self.assign('data', data)
		self.assign('selection', None)
		self.assign('index', None)
		self.assign('function')

	def size(self):
		return len(self.get('data'))
	
	def select(self):
		data=self.get('data')
		function=self.get('function')
		output=function(data)
		self.set('selection', output)
		return output

	def append(self, value):
		self.data.append(value)
		if self.over_capacity():
			del self.data[0]

	def over_capacity(self):
		return len(self.get('data')) < self.get('capacity')
