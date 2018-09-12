from math import atan2, sqrt, tanh
from goodata import Dict
from matrix import *
from settheory import equivalent, contains
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

class List:
	def __init__(self,data=[]):
		self.values=data
	def __getitem__(self, i):
		return self.value[i]
	def __setitem__(self, i, x):
		self.values[i]=x
	def append(self, x):
		self.values.append(x)
	def __call__(self,*x):
		return self.values
	def __repr__(self):
		return str(self.values)

class Unknown:
	def __repr__(self):return '<Unknown>'

class Empty:
	def __repr__(self):return '<Empty>'
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
EMPTY=Empty()
INF=Infinite()
FUNC=Func()
DATA=Data()
EXPR=Expr()
CONS=Cons()
SET='set'

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
	print(F,X)
	return F(X)

def eq_type(*X):
	for i in range(len(X)-1):
		x=X[i]
		y=X[i+1]
		if not (type(x) in [int, float] and type(y) in [int, float]) and type(x) != type(y):
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

def derivative(x,y):
	if eq_type(x,y):
		if isinstance(x, list) and len(x) == len(y):
			return [derivative(x[i],y[i]) for i in range(len(x))]
		elif isinstance(x, int) or isinstance(x, float):
			return x-y
	elif x==y:
		return 0

def rand_select(data):
	if isinstance(data,list) or isinstance(data,tuple):
		if len(data)>0:
			return data[rr(len(data))]
	elif isinstance(data,int):
		if data>0:return rr(data)

def nest(X):
	if len(X) > 1:
		Y=[]
		Y.append(X[0])
		Y.append(nest(X[1:]))
		return Y
	elif len(X) == 1:
		return [X[0]]

def flat(X):
	Y=[]
	if len(X) == 2:
		Y.append(X[0])
		if isinstance(X[1], list):
			Y+=flat(X[1])
		else:Y.append(X[1])
		return Y
	elif len(X) == 1:
		return [X[0]]

def compound(*data):
	keys=[]
	output=data[0]
	for i in range(1, len(data)):
		d=data[i]
		for j in d.keys():
			if j not in keys:
				output[j]=[d[j]]
				keys.append(j)
			elif d[j] not in output[j]:
				output[j]+=[d[j]]
	return output

def fill(source, *reference):
	output=Dict()
	for i in source.keys():
		output[i]=source[i]
		if output[i]==UNKNOWN:
			for j in range(len(reference)):
				print(reference)
				if i in reference[j].keys():
					output[i]=reference[j][i]
					break
	return output

def to_dict(keys=None, values=None):
	Y=Dict()
	if keys!=None:
		for i in range(len(keys)):
			k=keys[i]
			if values!=None:
				x=values[i]
			else:x=UNKNOWN
			Y[k]=x
	elif values!=None:
		for i in range(len(values)):
			k=i
			x=values[i]
			Y[k]=x
	return Y

def to_list(data, keys=None):
	Y=list()
	if keys==None:
		keys=data.keys()
	for i in keys:
		Y.append(data[i])
	return Y

def is_num(x):
	return isinstance(x, int) or isinstance(x, float)

def similarity(*data):
	output=0
	for i in range(len(data)-1):
		X=data[i]
		Y=data[i+1]
		y=0
		if eq_type(X,Y):
			if isinstance(X, list):
				count=0
				offset=abs(len(X)-len(Y))
				for i in range(len(X)):
					if i < len(Y):
						y += similarity(X[i], Y[i])
						count += 1
				if len(X)>0:
					y/=len(X)
			elif isinstance(X, dict):
				count=0
				Kx=list(X.keys())
				Ky=list(Y.keys())
				offset=len(compliment(Kx,Ky))+len(compliment(Ky,Kx))
				for i in Kx:
					if i in Ky:
						y += similarity(X[i], Y[i])
						count += 1
				if len(Kx)>0:
					y/=len(Kx)
			elif X == Y:
				y=1
		output += pow(y, 2)
	return sqrt(output)

def rand_list(size, data):
	Y=[]
	for i in range(size):
		y=rand_select(data)
		Y.append(y)
	return Y
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

def ERROR(X):
	total=0
	for i in range(len(X)-1):
		x=X[i]
		y=X[i+1]
		total+=pow(norm_error(x,y), 2)
	return sqrt(total)

def AND(*X):
	if len(X)==1 and isinstance(X[0], list) or isinstance(X[0], tuple):
		X=X[0]
	return False not in X
def OR(*X):
	if len(X)==1 and isinstance(X[0], list) or isinstance(X[0], tuple):
		X=X[0]
	return True in X
def NOT(*X):
	if len(X)==1 and isinstance(X[0], list) or isinstance(X[0], tuple):
		X=X[0]
	return True not in X

ALL=AND
SOME=OR
NO=NOT

def EQ(*X):
	if len(X)==1 and isinstance(X,list) or isinstance(X,tuple):
		X=X[0]
	if (isinstance(X, list) or isinstance(X, tuple)) and len(X)<2:
		return True
	elif isinstance(X, list):
		if X[0]==X[1]:
			return EQ(X[1:])
		return False
