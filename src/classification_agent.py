from space import *
from lib.base import *

class ClassificationAgent(Space):
	def __init__(self, function, state=1, classes=[]):
		super().__init__(ordered=False)
		if is_iter(function):
			keys=[]
			for i in range(len(function)):
				fi=function[i]
				if callable(fi):
					ki='f/'+str(i)
				else:ki=fi
				self.create(ki, fi)
				keys.append(ki)
			self.assign('function', keys)
		else:
			self.assign('function', function)
		self.assign('classes', list())
		self.assign('state', state)
	
	def __call__(self, x):
		y=UNKNOWN
		if self.get('state')==0:
			if x in self.keys():
				y=self.neighbors(x)
		else:
			y=self.classify(x)
			self.generate(x, y)
		return y

	def classify(self, x):
		k=self.get('function')
		if is_iter(k) or k in self.keys():
			f=self.retrieve('function')
		else:f=k
		if is_iter(f):
			y=[]
			for i in range(len(f)):
				fi=f[i]
				yi=fi(x)
				ki=k[i]
				if is_iter(yi):
					y+=yi
				elif yi:
					y.append(ki)
			if len(y)==1:y=y[0]
		else:y=f(x)
		return y

	def generate(self, x, y):
		if x not in self.keys():
			self.create(x)
		if is_iter(y):
			path=combine_rows(x,y)
		else:path=[(x,y)]
		for i in range(len(path)):
			self.connect(path[i])
			self.connect(reverse(path[i]))
