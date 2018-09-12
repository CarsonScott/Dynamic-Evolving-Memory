from model import *

class Function(Model):
	def __init__(self, function, inputs=[], interface=[], data=Dict(), strict=False):
		super().__init__()
		for i in interface:self[i]=UNKNOWN
		for i in inputs:self[i]=UNKNOWN
		self.assign('interface', interface)
		self.assign('function', function)
		self.assign('strict', strict)
		self.assign('inputs', inputs)
		for i in data.keys():
			self[i]=data[i]

	def __call__(self, *data):
		output=self.compute(*data)
		if not callable(self.get('function')):
			output=self.get('inputs'),output
		self.clear()
		return output

	def compute(self, *data):
		interface = self.get('interface')

		if isinstance(interface,list) or isinstance(interface,tuple):
			# data = list(data)
			if len(data)==len(interface):
				self.set(interface, data)
		if len(interface)==1:
			self.set(interface, data[0])
		if len(data)==1:
			data=data[0]
		f = self.retrieve('function')
		x = self.retrieve('inputs')
		for i in range(len(self.get('inputs'))):
			if isinstance(x[i], Function):
				variables = x[i].get('inputs')
				d = [UNKNOWN for i in variables]
				visited = []
				done = False
				while not done:
					if UNKNOWN in d:
						index = d.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = x[i].retrieve(variable)
							if not self.get('strict') and value == UNKNOWN:
								value = self.retrieve(variable)
								if value == UNKNOWN:
									value = variable
							d[index] = value
							visited.append(variable)
					else:done = True
				x[i].set(variables, d)
				variables = x[i].get('interface')
				d = [UNKNOWN for i in variables]
				visited = []
				done = False
				while not done:
					if UNKNOWN in d:
						index = d.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = self.retrieve(variable)
							if value == UNKNOWN and not self.get('strict'):
								value = x[i].retrieve(variable)
								if value == UNKNOWN:
									value = variable
							d[index] = value
							visited.append(variable)
					else:done = True
				x[i] = x[i](d)

		if not callable(f):
			return x
		if isinstance(f, Function):
			variables = f.get('inputs')
			d = [UNKNOWN for i in variables] 
			visited = []
			done = False
			while not done:
				if UNKNOWN in d:
					index = d.index(UNKNOWN)
					variable = variables[index]
					if variable not in visited:
						value = f.retrieve(variable)
						if value == UNKNOWN and not self.get('strict'):
							value = self.retrieve(variable)
							if value == UNKNOWN:
								value = variable
						d[index] = value
						visited.append(variable)
				else:done = True
			f.set(variables, d)
			variables = f.get('interface')
			d = self.retrieve(variables)
			visited = []
			done = False
			while not done:
				if UNKNOWN in d:
					index = d.index(UNKNOWN)
					variable = variables[index]
					if variable not in visited:
						value = f.retrieve(variable)
						if value == UNKNOWN and not self.get('strict'):
							value = self.retrieve(variable)
							if value == UNKNOWN:
								value = variable
						d[index] = value
						visited.append(variable)
				else:done = True
			x=d

		if len(x)==1:x=x[0]

		if isinstance(x, list) and len(x) == len(self.get('inputs')):
			try:
				return f(*x)
			except:
				raise Exception('FunctionError: ' + str(f) + ' could not compute: ' + merge(', ', x))
		return f(x)

	def clear(self):
		interface=self.get('interface')
		for i in interface:
			self[i]=UNKNOWN

def type_constraint(t):
	return Function(EQ, ['t','y'], ['x'], {'t':t,'y':Function(TYPE,['x'], ['x'])})