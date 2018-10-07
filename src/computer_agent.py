from agent import *

class Object(Model):
	def __init__(self, inputs=[], data=Dict()):
		self.inputs=inputs
		super().__init__()
		[self.assign(i, UNKNOWN) for i in inputs]
		[self.assign(i, data[i]) for i in data.keys()]

	def set_input(self, key, data=UNKNOWN):
		if key not in self.inputs:
			self.inputs.append(key)
		self.assign(key, data)

	def __call__(self, *data):
		output=Model()
		c=0
		is_inf=False
		if len(self.inputs)==1 and self.inputs[0]=='*':
			is_inf=True
			for i in range(len(data)):
				output[str(i)] = data[i]

		for i in self.keys():
			if (is_inf and i != '*') or not is_inf:
				if i in self.inputs:
					yi=data[c]
					c+=1
				else:yi=self[i]
				output[i]=yi
		return output

class ComputerAgent(Agent):
	def __init__(self):
		super().__init__()
		self.define('variables')
		self.define('functions')
		self.define('expressions')
		self.create('functions', 'get', Object(['key'], {'function':'get'}))
		self.create('functions', 'type-of', Object(['target'], {'function':'type-of'}))
		self.create('functions', 'size-of', Object(['target'], {'function':'size-of'}))
		self.create('functions', 'is-empty', Object(['target'], {'function':'is-empty'}))
		self.create('functions', 'in-class', Object(['key', 'class'], {'function':'in-class'}))
		self.create('functions', 'is-class', Object(['class'], {'function':'is-class'}))
		self.create('functions', 'is-full', Object(['target'], {'function':'is-full'}))
		self.create('functions', 'set', Object(['key', 'data'], {'function':'set'}))
		self.create('functions', 'pull-from', Object(['target'], {'function':'pull-from'}))
		self.create('functions', 'send-to', Object(['target', 'data'], {'function':'send-to'}))
		self.create('functions', 'get-classes', Object(['key'], {'function':'get_classes'}))
		self.create('functions', 'set-classes', Object(['key', 'class'], {'function':'set_classes'}))
		self.create('functions', 'set-attribute', Object(['key', 'attribute', 'data'], {'function':'set-attribute'}))
		self.create('functions', 'get-attribute', Object(['key', 'attribute'], {'function':'get-attribute'}))
		self.create('functions', 'define', Object(['class'], {'function':'define'}))
		self.create('functions', 'create', Object(['type', 'key', 'data'], {'function':'create'}))
		self.create('functions', 'compute', Object(['expression'], {'function':'reduce'}))
		self.create('functions', 'execute', Object(['data', 'function'], {'function':'execute'}))
		self.create('functions', 'select', Object(['constraint', 'options'], {'function':'select'}))
		self.create('functions', 'and', Object(['*'], {'function':AND}))
		self.create('functions', 'or', Object(['*'], {'function':OR}))
		self.create('functions', 'not', Object(['*'], {'function':NOT}))
		self.create('functions', 'add', Object(['*'], {'function':ADD}))
		self.create('functions', 'dif', Object(['*'], {'function':DIF}))
		self.create('functions', 'mul', Object(['*'], {'function':MUL}))
		self.create('functions', 'avg', Object(['*'], {'function':AVG}))
		self.create('functions', 'div', Object(['*'], {'function':DIV}))

	# Determine validity of syntactic expression
	def is_valid(self, expression):
		if is_type(expression, list):
			functions=self.meta['functions']
			if len(expression) >= 1:
				if is_type(expression[0], str):
					if expression[0] in functions:
						return True
		return False

	# Determine computability of function model 
	def is_computable(self, function):
		if is_type(function, Model):
			if not is_type(function, Object):
				if 'function' in function.keys():
					return True	
		return False

	# Convert expression into function model
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
	
	# Translate function model into function 
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

			elif f=='set-attribute':
				k=function['key']
				a=function['attribute']
				x=function['data']
				data=k,a,x
				func=self.set_attribute

			elif f=='get-attribute':
				k=function['key']
				a=function['attribute']
				data=k,a
				func=self.get_attribute
			
			elif f=='size-of':
				t=function['target']
				data=(t)
				func=self.size_of
			
			elif f=='type-of':
				t=function['target']
				data=(t)
				func=self.type_of
			
			elif f=='is-empty': 
				t=function['target']
				data=(t)
				func=self.is_empty
			
			elif f=='is-full':
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
			
			elif f=='set-classes':
				k=function['key']
				c=function['class']
				data=k,c
				func=self.set_classes

			elif f=='get-classes':
				k=function['key']
				data=(k)
				func=self.get_classes

			elif f=='in-class':
				k=function['key']
				c=function['class']
				data=k,c
				func=self.in_class

			elif f=='is-class':
				c=function['class']
				data=(c)
				func=self.is_class

			elif f=='reduce':
				e=function['expression']
				data=(e)
				func=self.reduce

			elif f=='execute':
				x=function['data']
				g=function['function']
				data=x,g
				func=self.execute

			elif f=='select':
				g=function['constraint']
				x=function['options']
				data=g,x
				func=self.select

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

	# Apply function to inputs
	def execute(self, data, func):
		for i in range(len(data)):
			if self.is_computable(data[i]):
				x,f=self.convert(data[i])
				data[i]=self.execute(x,f)
		return func(*data)
		
	# Convert expression into function and compute output
	def compute(self, expression):
		if is_type(expression, str):
			if self.in_class(expression, 'expressions'):
				expression=self.get(expression)
		function=self.reduce(expression)
		data,func=self.convert(function)
		output=self.execute(data,func)
		return output

	# determine options that satisfy constraint
	def select(self, constraint, options):
		data=[self[i] for i in options if i in self]
		if constraint in self: 
			function=self[constraint]
		else:function=constraint

		indices=filter(function, *data)
		outputs=[]
		for i in indices:
			oi=options[i]
			outputs.append(oi)
		return outputs	

	# Convert expression into sentence
	def encode(self, expression):
		words=combine_elements(expression)
		sentence=merge(' ', words)
		return sentence
		