from space import *
from lib.base import *

class MemoryAgent(Space):
	# buffer is a model of the state of measurements at time t. 
	# memory is a model of the state sequence from time t-n to t.
	def __init__(self, memory_size=1, buffer_size=1, metadata=Dict()):
		super().__init__(ordered=True)
		self.meta=Model()
		self.meta.assign('memory-size', memory_size)
		self.meta.assign('buffer-size', buffer_size)
		for i in metadata.keys():
			self.meta[i]=metadata[i]

		self.assign('functions', EMPTY)
		self.assign('memory', Dict())
		self.assign('buffer', [])
		self.assign('removed', [])
		self.assign('overflow', [])
		self.assign('step', 0)

	def __call__(self, *x):
		self.step()
		f=self['functions']
		if f!=EMPTY:
			if is_iter(f):
				data=[]
				for i in range(len(f)):
					fi=f[i]
					yi=fi(x)
					data.append(yi)
			elif callable(f):
				data=f(x)
		data=x
		self.store_buffer_data(data)
		self.update_buffer_data()
		self.store_memory_data()
		self.update_memory_data()

	def step(self):
		self['step']+=1

	def store_buffer_data(self, data):
		self['buffer'].append(data)
	
	def update_buffer_data(self):
		if len(self['buffer']) > self.meta['buffer-size']:
			error=len(self['buffer']) > self.meta['buffer-size']
			del self['buffer'][0:abs(error)-1]
			index=0
			data=self['buffer'].pop(index)
			self['overflow'].append(data)

	def store_memory_data(self):
		data=list(self['buffer'])
		self['memory'][self['step']]=data
	
	def update_memory_data(self):
		if len(self['memory']) > self.meta['memory-size']:
			index = self['step'] - self.meta['memory-size']
			data=self['memory'].pop(index)
			self['removed'].append(data)
