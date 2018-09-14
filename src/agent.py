from lib.base import *
from space import *

class Object(Model):
	def __init__(self, inputs=[], data=Dict()):
		self.inputs=inputs
		super().__init__()
		[self.assign(i, UNKNOWN) for i in inputs]
		[self.assign(i, data[i]) for i in data.keys()]
	def __call__(self, *data):
		output=Model()
		c=0
		for i in self.keys():
			if i in self.inputs:
				yi=data[c]
				c+=1
			else:yi=self[i]
			output[i]=yi
		if c==len(self.inputs):
			return output

class Agent(Space):
	def __init__(self, data=Model(), meta=Model()):
		super().__init__()
		self.meta=Model()
		[self.meta.assign(i, meta[i]) for i in meta.keys()]
		[self.assign(i, data[i]) for i in data.keys()]

	def __call__(self, data):
		return data

	def send_to(self, target, data):
		self[target].append(data)
		return self[target]
	def pull_from(self, target):
		return self[target].pop()
	def set_capacity(self, target, size):
		self.meta[str(target)+'-size'] = size
	def get_capacity(self, target):
		return self.meta[str(target)+'-size']
	def size_of(self, target):
		return len(self[target])
	def type_of(self, target):
		return type(self[target])
	def is_empty(self, target):
		return self.size_of(target)==0
	def is_full(self, target):
		return self.size_of(target)==self.get_capacity(target)

class ComputerAgent(Agent):
	def __init__(self, data=Model(), meta=Model()):
		super().__init__(data, meta)
		self.meta.assign('functions', [])
		self.create('send-to', Object(['target', 'data'], {'function':'send-to'}))
		self.create('pull-from', Object(['target'], {'function':'pull-from'}))
		self.create('size-of', Object(['target'], {'function':'size-of'}))
		self.create('type-of', Object(['target'], {'function':'type-of'}))
		self.create('is-empty', Object(['target'], {'function':'is-empty'}))
		self.create('is-full', Object(['target'], {'function':'is-full'}))
		self.create('set', Object(['key', 'data'], {'function':'set'}))
		self.create('get', Object(['key'], {'function':'get'}))

	def __call__(self, expression):
		function=self.reduce(expression)
		output=self.compute(function)
		return output
	
	def is_valid(self, expression):
		if isinstance(expression, list):
			functions=self.meta['functions']
			if len(expression) >= 1:
				if isinstance(expression[0], str):
					if expression[0] in functions:
						return True
		return False

	def is_computable(self, function):
		if isinstance(function, Model):
			if 'function' in function.keys():
				return True
		return False

	def create(self, key, function=Object()):
		self.meta['functions'].append(key)
		self.assign(key, function)

	def reduce(self, data):
		if self.is_valid(data):
			x=[]
			for i in range(len(data)):
				xi=data[i]
				if i==0 and xi in self:
					xi=self[xi]
				if self.is_valid(xi):
					xi=self.reduce(xi)
				x.append(xi)
			f=x[0]
			x=x[1:]
			return f(*x)

	def compute(self, function):
		if self.is_computable(function):
			f=function['function']
			if f=='send-to':
				t=function['target']
				x=function['data']
				data=t,x
				func=self.send_to
			elif f=='pull-from': 
				t=function['target']
				data=(t)
				func=self.pull_from
			elif f=='size-of':
				t=function['target']
				data=(t)
				func=self.size_of
			elif f=='type-of':
				t=function['target']
				data=(t)
				func=self.type_of
			elif f=='is_empty': 
				t=function['target']
				data=(t)
				func=self.is_empty
			elif f=='is_full':
				t=function['target']
				data=(t)
				func=self.size_of
			elif f=='set':
				k=function['key']
				x=function['data']
				data=k,x
				func=self.__setitem__
			elif f=='get':
				k=function['key']
				data=(k)
				func=self.__getitem__
			elif not callable(f):
				return UNKNOWN
			else:
				func=f
				data=[]
				for i in function.keys():
					if i != 'function':
						xi=function[i]
						if is_type(xi, str) and xi in self:
							xi=self[xi]
						data.append(xi)

			data=list(data)
			for i in range(len(data)):
				if self.is_computable(data[i]):
					data[i]=self.compute(data[i])
			return func(*data)
		else:return UNKNOWN
