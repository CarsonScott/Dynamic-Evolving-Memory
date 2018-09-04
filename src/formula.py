from function import *

class Formula(Model):
	def __init__(self, function, arity=INF):
		super().__init__()
		if arity!=INF:
			constraints=[]
			for i in range(arity):
				constraints.append([])
		else:constraints=[]
		self.assign('arity', arity)
		self.assign('function', function)
		self.assign('constraints', constraints)

	def __call__(self, *data):
		if self.check(*data):
			function=str(self.get('function'))
			inputs=['x'+str(i) for i in range(len(data))]
			expression=Function(function, inputs)
			expression.set(inputs,data)
			return expression
		return None

	def check(self, *data):
		constraints=self.get('constraints')
		arity=self.get('arity')
		if arity==INF:constraints=[constraints for i in range(len(data))]
		elif len(data)!=arity:return False
		for i in range(len(constraints)):
			f=constraints[i]
			x=data[i]
			if len(f)>0 and not AND(apply(f,x)):
				return False
		return True

	def append(self, index, constraint):
		self['constraints'][index].append(constraint)
