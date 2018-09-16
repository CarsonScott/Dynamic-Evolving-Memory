from lib.base import *
from model import *

def filter(f, *x):
	y=[]
	for i in range(len(x)):
		xi=x[i]
		yi=f(xi)
		if yi==True:
			y.append(i)
	return y

def AND(*x):
	return False not in x
def OR(*x):
	return True in x
def ADD(*x):
	return sum(x)
def DIF(*x):
	return x[1]-x[0]

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

class Agent(Model):
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


# a=ComputerAgent()
# print(a.compute(['define', 'new_class']))
# print(a.compute(['create', 'new_class', 'x', 34]))
# print(a.compute(['create', 'functions', 'add', Object(['a', 'b'], {'function':add})]))
# print(a.compute(['add', 5, 6]))
# print(a.compute(['get', 'x']))
# print(a.compute(['define', 'c1']))
# print(a.compute(['set_classes', 'x', 'c1']))
# print(a.meta)
# print()

# a.create('expressions', 'e1', ['add', 45, 5])
# print(a.compute('e1'))

# print(a.meta['functions'])

