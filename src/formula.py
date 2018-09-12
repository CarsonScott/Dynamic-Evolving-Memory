from function import *

class Formula(Model):
	def __init__(self, function, arity=INF, constraints=Dict()):
		super().__init__()
		inputs=Dict()
		if arity!=INF:
			for i in range(arity):
				inputs[i]=[]
				if i in constraints.keys():
					c=constraints[i]
					if not isinstance(c,list):
						c=[c]
					inputs[i]+=c
		if '*' in constraints.keys():
			C=constraints['*']
			if not isinstance(C,list):
				C=[C]
			inputs['*']=C
		self.assign('arity', arity)
		self.assign('function', function)
		self.assign('constraints', inputs)

	def __call__(self, *data):
		if self.check(*data):
			function=self.get('function')
			inputs=[str(i) for i in range(len(data))]
			expression=Function(function, inputs)
			expression.set(inputs, data)
			return expression
		return None

	def check(self, *data):
		arity=self.get('arity')
		constraints=self.get('constraints')
		if arity!=INF and len(data)!=arity:
			return False
		for i in range(len(data)):
			x=data[i]
			if arity!=INF:
				f=list(constraints[i])
				if not AND(apply(f,x)):
					return False
			if '*' in constraints.keys():
				u=(constraints['*'])
				if not AND(apply(u, x)):
					return False
		return True

	def append(self, index, constraint):
		self['constraints'][index].append(constraint)
		

def create_formula(data):
	if isinstance(data, Dict) and contains(data.keys(), ['arity', 'function', 'constraints']):
		a=data['arity']
		f=data['function']
		c=data['constraints']
		F=Formula(f,a)
		for i in data.keys():
			F.set(i, data[i])
		return F
def compose_function(data):
	if isinstance(data,list):
		output=[]
		for i in range(len(data)):
			output.append(compose_function(data[i]))
		return output
	elif isinstance(data,tuple):
		for i in range(len(data)-1):
			a=data[i]
			b=data[i+1]
			if isinstance(a, Dict) and isinstance(b, list):
				formula=create_formula(a)
				inputs=compose_function(b)
				function=formula(*inputs)
				return function
	else:return data