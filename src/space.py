from lib.util import *
from model import *

class Space(Model):
	def __init__(self):
		super().__init__()
		self.assign('neighbors', Dict())
		self.assign('paths', list())
		self.assign('keys', list())

	def order(self, keys):
		order=self.get('keys')
		indices=[]
		for i in keys:
			if i in order:
				indices.append(order.index(i))
			else:indices.append(-1)
		return tuple([keys[i] for i in sort(indices)])

	def create(self, key, obj=UNKNOWN):
		self['keys'].append(key)
		self['neighbors'][key]=Dict()
		self[key]=obj

	def connect(self, keys, rel=UNKNOWN):
		keys=self.order(keys)
		path=nest(keys)
		self['paths'].append(path)
		for i in range(len(keys)-1):
			k1=keys[i]
			k2=keys[i+1]
			self['neighbors'][k1][k2]=rel

	def traverse(self, path):
		return self.retrieve(flat(path))

