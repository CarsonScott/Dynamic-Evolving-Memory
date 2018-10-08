from agent import *

def dimension(name, type=None):
	dim=Model()
	dim.assign('name', name)
	dim.assign('type', type)
	return dim

class Schema(Agent):
	def __init__(self, *dimensions):
		super().__init__()
		self.define('dimensions')
		for i in range(len(dimensions)):
			dim=dimensions[i]
			if is_iter(dim) and len(dim)==2:
				dim=dimension(*dim)
			type=dim['type']
			name=dim['name']
			self.create('dimensions', name, type)
	
	def __call__(self, values=[]):
		dimensions=self.meta['dimensions']
		instance=Model()
		for i in range(len(values)):
			ki=dimensions[i]
			xi=values[i]
			ti=self[ki]
			valid=True
			if isinstance(ti, type) and not isinstance(xi,ti):
				error_message='DimensionError: \'' + ki + '\' dimension must be of type ' + str(ti) + '; recieved type ' + str(type(xi)) + '.'
				raise Exception(error_message)
			else:instance.assign(ki,xi)
		return instance

# class Schema(Model):
# 	def __init__(self,  process=[], inputs=[], outputs=[], relations=Dict(), *data):
# 		super().__init__(*data)
# 		self.assign('process', process)
# 		self.assign('relations', relations)
# 		self.assign('inputs', inputs)
# 		self.assign('outputs', outputs)
# 	def execute(self, function):
# 		function=self.retrieve(function)
# 		if isinstance(function,Function):
# 			interface=to_dict(function.get('interface'))
# 			values=fill(interface, self)
# 			values=to_list(values)
# 			output=function(values)
# 			f=function.get('function')
# 			relations=self.get('relations').keys()
# 			if f in relations:
# 				operation=self[f]
# 				inputs,values=output
# 				for i in range(len(inputs)):
# 					k=inputs[i]
# 					x=values[i]
# 					if x==UNKNOWN:
# 						values[i]=k
# 				output=operation(*values)
# 			return output

# 	def __call__(self, *data):
# 		inputs=self.get('inputs')
# 		for i in range(len(inputs)):
# 			self[inputs[i]]=data[i]
# 		values=[]
# 		functions=self.get('process')
# 		for f in functions:
# 			values.append(self.execute(f))
# 		outputs=self.get('outputs')
# 		if outputs!=[]:
# 			values=self.retrieve(outputs)
# 		return values
