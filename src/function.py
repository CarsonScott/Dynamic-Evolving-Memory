from model import *

class Function(Model):
	def __init__(self, function, inputs=[], interface=[], data=Dict()):
		super().__init__()
		for i in interface:self[i]=UNKNOWN
		for i in inputs:self[i]=UNKNOWN
		self.assign('interface', interface)
		self.assign('function', function)
		self.assign('inputs', inputs)

		for i in data.keys():
			self[i]=data[i]

	def __call__(self, *data):
		interface = self.get('interface')
		if len(data)==1:data=data[0]
		if isinstance(data,list) or isinstance(data,tuple):
			data = list(data)
			if len(data)==len(interface):
				self.set(interface, data)
		elif isinstance(interface,list) or isinstance(interface,tuple):
			if len(interface)==1:
				self.set(interface[0], data)

		f = self.retrieve('function')
		x = self.retrieve('inputs')
		for i in range(len(self.get('inputs'))):
			if isinstance(x[i], Function):
				variables = x[i].get('inputs')
				data = [UNKNOWN for i in variables]

				visited = []
				done = False
				while not done:
					if UNKNOWN in data:
						index = data.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = x[i].retrieve(variable)
							if value == UNKNOWN:
								value = self.retrieve(variable)
								if value == UNKNOWN:
									value = variable
							data[index] = value
							visited.append(variable)
					else:done = True
				x[i].set(variables, data)
				variables = x[i].get('interface')
				data = [UNKNOWN for i in variables]
				visited = []
				done = False
				while not done:
					if UNKNOWN in data:
						index = data.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = self.retrieve(variable)
							if value == UNKNOWN:
								value = x[i].retrieve(variable)
								if value == UNKNOWN:
									value = variable
							data[index] = value
							visited.append(variable)
					else:done = True
				x[i] = x[i](data)
		if f == 'set':
			key = x[0]
			value = x[1]
			if isinstance(key, Constant):
				key = key.value
			self[key] = value
		elif callable(f):
			if isinstance(f, Function):
				variables = f.get('inputs')
				data = [UNKNOWN for i in variables]
				visited = []
				done = False
				while not done:
					if UNKNOWN in data:
						index = data.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = f.retrieve(variable)
							if value == UNKNOWN:
								value = self.retrieve(variable)
								if value == UNKNOWN:
									value = variable
							data[index] = value
							visited.append(variable)
					else:done = True
				f.set(variables, data)
				variables = f.get('interface')
				data = [UNKNOWN for i in variables]
				visited = []
				done = False
				while not done:
					if UNKNOWN in data:
						index = data.index(UNKNOWN)
						variable = variables[index]
						if variable not in visited:
							value = f.retrieve(variable)
							if value == UNKNOWN:
								value = self.retrieve(variable)
								if value == UNKNOWN:
									value = variable
							data[index] = value
							visited.append(variable)
					else:done = True
				if isinstance(x, tuple):
					x = tuple(data)
				else:x = data
			if isinstance(x, tuple):
				return f(*x)
			else:return f(x)
		