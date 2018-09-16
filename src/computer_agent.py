from agent import *

class ComputerAgent(Agent):
	def __init__(self):
		super().__init__()
		self.define('functions')
		self.create('functions', 'send-to', Object(['target', 'data'], {'function':'send-to'}))
		self.create('functions', 'set-capacity', Object(['target', 'size'], {'function':'set-capacity'}))
		self.create('functions', 'get-capacity', Object(['target'], {'function':'get-capacity'}))
		self.create('functions', 'pull-from', Object(['target'], {'function':'pull-from'}))
		self.create('functions', 'size-of', Object(['target'], {'function':'size-of'}))
		self.create('functions', 'type-of', Object(['target'], {'function':'type-of'}))
		self.create('functions', 'is-empty', Object(['target'], {'function':'is-empty'}))
		self.create('functions', 'is-full', Object(['target'], {'function':'is-full'}))
		self.create('functions', 'set', Object(['key', 'data'], {'function':'set'}))
		self.create('functions', 'get', Object(['key'], {'function':'get'}))
		self.create('functions', 'create', Object(['type', 'key', 'data'], {'function':'create'}))
		self.create('functions', 'define', Object(['class'], {'function':'define'}))
		self.create('functions', 'set_classes', Object(['key', 'class'], {'function':'set_classes'}))
		self.create('functions', 'get_classes', Object(['key'], {'function':'get_classes'}))
		self.create('functions', 'compute', Object(['expression'], {'function':'reduce'}))
		self.create('functions', 'execute', Object(['data', 'function'], {'function':'execute'}))
		self.create('functions', 'select', Object(['*'], {'function':self.select}))
		self.create('functions', 'and', Object(['*'], {'function':AND}))
		self.create('functions', 'or', Object(['*'], {'function':OR}))
		self.create('functions', 'add', Object(['*'], {'function':ADD}))
		self.create('functions', 'dif', Object(['*'], {'function':DIF}))

	def is_valid(self, expression):
		if is_type(expression, list):
			functions=self.meta['functions']
			if len(expression) >= 1:
				if is_type(expression[0], str):
					if expression[0] in functions:
						return True
		return False

	def is_computable(self, function):
		if is_type(function, Model):
			if not is_type(function, Object):
				if 'function' in function.keys():
					return True	
		return False

	def reduce(self, expression):
		if self.is_valid(expression):
			x=[]
			for i in range(len(expression)):
				xi=expression[i]
				if i==0 and xi in self:
					xi=self[xi]
				if self.is_valid(xi):
					xi=self.reduce(xi)
				x.append(xi)
			f=x[0]
			x=x[1:]
			function=f(*x)
			return function
		return UNKNOWN
	
	def convert(self, function):
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

			elif f=='set-capacity':
				t=function['target']
				s=function['size']
				data=t,s
				func=self.set_capacity

			elif f=='get-capacity':
				t=function['target']
				data=(t)
				func=self.get_capacity
			
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
			
			elif f=='create':
				t=function['type']
				k=function['key']
				x=function['data']
				data=t,k,x
				func=self.create
			
			elif f=='define':
				c=function['class']
				data=(c)
				func=self.define
			
			elif f=='set_classes':
				k=function['key']
				c=function['class']
				data=k,c
				func=self.set_classes

			elif f=='get_classes':
				k=function['key']
				data=(k)
				func=self.get_classes

			elif f=='reduce':
				e=function['expression']
				data=(e)
				func=self.reduce

			elif f=='execute':
				x=function['data']
				g=function['function']
				data=x,g
				func=self.execute

			elif callable(f):
				func=f
				data=[]
				for i in function.keys():
					if i != 'function':
						xi=function[i]
						if is_type(xi, str) and xi in self:
							xi=self[xi]
						data.append(xi)
			else:return UNKNOWN

			if not is_iter(data):
				data=[data]
			elif not is_type(data, list):
				data=list(data)
			return data, func
		else:return UNKNOWN, UNKNOWN

	def execute(self, data, func):
		for i in range(len(data)):
			if self.is_computable(data[i]):
				x,f=self.convert(data[i])
				data[i]=self.execute(x,f)
		return func(*data)
		
	def compute(self, expression):
		if is_type(expression, str):
			if self.in_class(expression, 'expressions'):
				expression=self.get(expression)
		function=self.reduce(expression)
		data,func=self.convert(function)
		output=self.execute(data,func)
		return output
