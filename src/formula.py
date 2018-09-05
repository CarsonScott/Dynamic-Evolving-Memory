from function import *

def type_constraint(t):
	return Function(EQ, ['t','y'], ['x'], {'t':t,'y':Function(TYPE,['x'],['x'])})

# class Association(Model):
# 	def __init__(self, relation, arity=INF, constraints=Dict()):
# 		super().__init__()
# 		if arity!=INF:
# 			inputs=[]
# 			for i in range(arity):
# 				inputs.append([])
# 		else:inputs=[[]]

# 		for i in constraints.keys():
# 			inputs[i]=constraints[i]
	
# 		self.assign('arity', arity)
# 		self.assign('relation', relation)
# 		self.assign('constraints', inputs)

# 	def __call__(self, *data):
# 		if self.check(*data):
# 			relation=self.get('relation')
# 			inputs=[str(i) for i in range(len(data))]
# 			expression=relation,inputs
# 			return expression
			
# 		return None

# 	def check(self, *data):
# 		arity=self.get('arity')
# 		constraints=self.get('constraints')
# 		if arity!=INF and len(data)!=arity:
# 			return False
# 		for i in range(len(data)):
# 			if arity==INF:
# 				f=constraints[0]
# 			else:f=constraints[i]
# 			x=data[i]
# 			if f!=[] and not AND(apply(f,x)):
# 				return False
# 		return True

# 	def append(self, index, constraint):
# 		self['constraints'][index].append(constraint)
	
# 	def check(self, *data):
# 		arity=self.get('arity')
# 		constraints=self.get('constraints')
# 		if arity!=INF and len(data)!=arity:
# 			return False

# 		for i in range(len(data)):
# 			x=data[i]
# 			if arity!=INF:
# 				f=list(constraints[i])
# 				if not AND(apply(f,x)):
# 					return False
			
# 			if '*' in constraints.keys():
# 				u=list((constraints['*']))
# 				if not AND(apply(u, x)):
# 					return False
# 		return True

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
