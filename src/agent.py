from lib.base import *
from space import *

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

class Translation(Object):
	def __init__(self, phrase=EMPTY, result=EMPTY):
		inputs=[]
		data={}
		if phrase==EMPTY:inputs.append('phrase')
		else:data['phrase']=phrase
		if result==EMPTY:inputs.append('result')
		else:data['result']=result
		super().__init__(['phrase', 'result'], data)

print(Translation('a + b', 4))

class Agent(Space):
	def __init__(self):
		super().__init__()
		self.meta=Model()
	def send_to(self, target, data):
		self[target].append(data)
		return self[target]
	def pull_from(self, target):
		return self[target].pop()
	def del_from(self, target, index):
		del self[target][index]
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
	def is_class(self, name):
		return name in self.meta and is_type(self.meta[name], list)
	def in_class(self, key, name):
		if self.is_class(name):
			return key in self.meta[name]
	def define(self, name):
		self.meta[name]=[]
	def create(self, type, key, data):
		self.set_classes(key, type)
		self.assign(key, data)
	def set_classes(self, key, name):
		if is_type(name, list):
			for i in range(len(name)):
				ni=name[i]
				self.set_classes(key, ni)
		elif self.is_class(name):
			if not self.in_class(key, name):
				self.meta[name].append(key)
	def get_classes(self, key):
		classes=[]
		for i in self.meta.keys():
			if self.in_class(key, i):
				classes.append(i)
		return classes

def AND(*x):
	print(x)
	return False not in x
def OR(*x):
	return True in x
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
		self.create('functions', 'and', Object(['*'], {'function':AND}))
		self.create('functions', 'or', Object(['*'], {'function':OR}))

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

class MemoryAgent(ComputerAgent):
	
	def __init__(self, memory_size=UNKNOWN):
		super().__init__()
		self.define('inputs')
		self.define('mutable')
		self.define('main')
		self.create('mutable', 'memory', [])
		self.create('mutable', 'buffer', [])
		self.create('mutable', 'output', [])
		if memory_size!=UNKNOWN:
			self.set_capacity('memory', memory_size)

	def is_valid(self, expression):
		if is_type(expression, tuple):
			for i in range(len(expression)):
				ei=expression[i]
				if not self.is_valid(ei):
					return False
			return True
		return super().is_valid(expression)

	def compute(self, expression, root=True):
		if is_type(expression, str):
			if self.in_class(expression, 'expressions'):
				expression=self.get(expression)
		if root:self.update_buffer(expression)
		
		if is_type(expression, tuple):
			outputs=[]
			for i in range(len(expression)):
				ei=expression[i]
				yi=self.compute(ei, root=False)
				outputs.append(yi)
			return outputs
		else:return super().compute(expression)

	def update_buffer(self, expression):
		words=combine_elements(expression)
		sentence=merge(' ', words)
		self.send_to('buffer', sentence)

	def update_memory(self):
		words=self['buffer']
		sentences=combine_elements(words)
		phrase=merge(', ', sentences) + ';'
		if self.is_full('memory'):
			self.del_from('memory', 0)
		self.send_to('memory', phrase)
		self['buffer']=[]
		return self['memory']

	def update_output(self, data):
		buffer=self['buffer']
		output=combine_rows(buffer, data)
		self['output']=[]
		for i in range(len(output)):
			yi=output[i]
			yi=Translation(*yi)
			self.send_to('output', yi)
		# self['output']=output
		return self['output']

	def update(self, *data):
		inputs=self.meta['inputs']
		for i in range(len(data)):
			xi=data[i]
			ki=inputs[i]
			self[ki]=xi
		outputs=[]
		functions=self.meta['main']
		for i in functions:
			expression=self[i]
			output=self.compute(expression)
			if output==None:
				output=EMPTY
			outputs.append(output)
		output=self.update_output(outputs)
		memory=self.update_memory()
		return output


class GoalAgent(MemoryAgent):
	def select(self, constraint, options):
		indices=filter(constraint, *options)
		outputs=[]
		for i in indices:
			oi=options[i]
			outputs.append(oi)
		return outputs	

def add(*x):
	return sum(x)
def dif(*x):
	return x[1]-x[0]

def filter(f, *x):
	y=[]
	for i in range(len(x)):
		xi=x[i]
		yi=f(xi)
		if yi==True:
			y.append(i)
	return y
