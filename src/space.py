from lib.util import *

class Space(Dict):
	def __init__(self):
		self.values = Dict()

	def set(self, key, value, neighborhood=[]):
		if key not in self.keys():
			self.values[key]=UNKNOWN
			self[key]=[]
		self.values[key]=value
		for i in range(len(neighborhood)):
			k=neighborhood[i]
			if k not in self[key]:
				self[key].append(k)	

	def get(self, key):
		return self.values[key]
