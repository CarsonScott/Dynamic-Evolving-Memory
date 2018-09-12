from lib.util import *

def is_type(x, type):
	return isinstance(x, type)
def is_tuple(x):
	return is_type(x, tuple)
def is_list(x):
	return is_type(x, list)
def is_int(x):
	return is_type(x, int)
def is_float(x):
	return is_type(x, float)
def is_bool(x):
	return is_type(x, bool)

def is_num(x):
	return is_int(x) or is_float(x)
def is_iter(x):
	return is_list(x) or is_tuple(x)
def eq_len(x,y):
	return len(x)==len(y)
def eq_val(x, y):
	return x==y
def eq_type(x, y):
	return is_type(x, type(y)) or is_type(y, type(x))
def is_true(x):
	return is_bool(x) and x
def is_false(x):
	return not is_true(x)

def call(f, *x):
	return f(*x)

def rcall(f,*x):
	if len(x)==1:
		if is_iter(x[0]):
			x=x[0]
			return call(f, x)
		else:
			return call(f, x[0])
	else:return rcall(f, *x[:1])

def tolist(x):
	if is_list(x):
		return x
	if is_tuple(x):
		return list(x)
	return [x]
def totuple(x):
	if is_tuple(x):
		return x
	if is_list(x):
		return tuple(x)
	return (x)
def toint(x):
	if is_int(x):
		return x
	if is_float(x):
		return int(x)
def tofloat(x):
	if is_float(x):
		return x
	if is_int(x):
		return float(x)

def combine_elements(x):
	y=[]
	if is_iter(x):
		for i in range(len(x)):
			xi=x[i]
			yi=tolist(xi)
			y=y+yi
	return y

def combine_consecutive(x):
	y=[]
	if is_iter(x):
		for i in range(len(x)-1):
			j=i+1
			xi=x[i]
			xj=x[j]
			yi=xi,xj
			y.append(yi)
	return y

def combine_rows(x, y):
	z=[]
	if is_iter(x):
		for i in range(len(x)):
			xi=x[i]
			yi=y
			if is_iter(y):
				yi=y[i]
			zi=xi,yi
			z.append(zi)				
	elif is_iter(y):
		for i in range(len(y)):
			xi=x
			yi=y[i]
			zi=xi,yi
			z.append(zi)
	else:z=x,y
	return z

def combine_columns(x):
	z=[]
	if is_iter(x) and rcall(eq_len, x):
		for i in range(len(x)-1):
			j=i+1
			xi=x[i]
			xj=x[j]
			if eq_len(xi,xj):
				for k in range(len(xi)):
					if k >= len(z):
						z.append([])
					z[k].append(xi[k])
					z[k].append(xj[k])
	return z

def all_true(x):
	if is_iter(x): return rcall(is_true, x)
def none_true(x):
	if is_iter(x): return rcall(is_false, x)
def some_true(x):
	if is_iter(x): 
		if all_true(x):
			return True
		if not none_true(x):
			return True
	return False

def similarity(x, y):
	r=0
	s=1
	if is_iter(x) and is_iter(y):
		s=len(x)+len(y)
		for i in range(len(x)):
			xi=x[i]
			ri=0
			if xi in y:
				ri=1					
			if xi in y:
				r+=ri
	elif is_iter(x):
		s=len(x)+1
		if y in x:
			r=1
	elif is_iter(y):
		s=len(y)+1
		if x in y:
			r=1
	else:
		s=1
		if x is y:
			r=1
	y=r/s * 2
	return y

def norm_similarity(*x):
	x=combine_consecutive(x)
	y=0
	for i in range(len(x)):
		xi=x[i]
		yi=similarity(*xi)
		dy=pow(yi, 2)
		y+=dy
	y=sqrt(y)
	return y

def mean_similarity(*x):
	x=combine_consecutive(x)
	y=0
	for i in range(len(x)):
		xi=x[i]
		yi=similarity(*xi)
		dy=yi * 1/len(x)
		y+=dy
	return y