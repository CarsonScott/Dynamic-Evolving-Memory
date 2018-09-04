from math import atan2, sqrt, tanh
from goodata import Dict
from matrix import *
from settheory import equivalent
from utilities import sort, rr, merge, logistic, softmax
from functions import *

class Constant:
	def __init__(self, value):
		self.value=value
	def __call__(self):
		return self.value

class Lock:
	def __init__(self, value, constraint):
		self.value=value
		self.constraint=constraint
	def __call__(self, data):
		if self.constraint(data):
			return self.value
		else:return UNKNOWN

class Unknown:
	def __repr__(self):return '<Unknown>'
class Infinite:
	def __repr__(self):return '<Infinite>'
class Func:
	def __repr__(self):return '<Function>'
class Data:
	def __repr__(self):return '<Data>'
class Expr:
	def __repr__(self):return '<Expression>'
class Cons:
	def __repr__(self):return '<Constant>'

UNKNOWN=Unknown()
INF=Infinite()
FUNC=Func()
DATA=Data()
EXPR=Expr()
CONS=Cons()

def eq_type(x,y):
	if type(x) != type(y):
		if type(x) in [int, float] and type(y) in [int, float]:
			return True
		return False
	return True

def norm_error(x,y, root=True):
	if eq_type(x,y):
		if isinstance(x, Dict) and equivalent(x.keys(), y.keys()):
			diff = 0
			for i in x.keys():
				diff += norm_error(x[i], y[i], False)
			return sqrt(diff)
		elif isinstance(x, list) and len(x) == len(y):
			diff = 0
			for i in range(len(x)):
				diff += norm_error(x[i], y[i], False)
			return sqrt(diff)
		elif isinstance(x, int) or isinstance(x, float):
			diff = pow(x-y, 2)
			if root:return sqrt(diff)
			return diff
	diff = int(x!=y)
	if root:diff = sqrt(diff)
	return diff

def TRUE(x):
	return True

def FALSE(x):
	return False

def TYPE(x):
	if isinstance(x,list) or isinstance(x,tuple):
		y=[type(x[i]) for i in range(len(x))]
		if len(y)==1:
			y=y[0]
	else:y=type(x)
	return y

def AND(*X):
	if len(X)==1 and isinstance(X[0], list) or isinstance(X[0], tuple):
		X=X[0]
	return False not in X
def OR(*X):
	if len(X)==1 and isinstance(X[0], list) or isinstance(X[0], tuple):
		X=X[0]
	return True in X

def product(X):
	x = X[0]
	for i in range(1, len(X)):
		x *= X[i]
	return x

def average(X):
	if len(X) > 0:
		return sum(X)/len(X)
	return 0

def apply(F,X):
	Y=[]
	if isinstance(F, list) or isinstance(F, tuple):
		x=X
		for i in range(len(F)):
			f=F[i]
			if isinstance(X, tuple) and len(F)==len(X):
				x=X[i]
			Y.append(apply(f,x))
		return Y
	elif isinstance(X, tuple):
		f=F
		for i in range(len(X)):
			x=X[i]
			Y.append(apply(f,x))
		return Y
	return F(X)

