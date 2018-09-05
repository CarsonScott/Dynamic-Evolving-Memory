from function import *

class Schema(Model):
	def __init__(self,  process=[], inputs=[], outputs=[], relations=Dict(), *data):
		super().__init__(*data)
		self.assign('process', process)
		self.assign('relations', relations)
		self.assign('inputs', inputs)
		self.assign('outputs', outputs)
	def execute(self, function):
		function=self.retrieve(function)
		if isinstance(function,Function):
			interface=to_dict(function.get('interface'))
			values=fill(interface, self)
			values=to_list(values)
			output=function(values)
			f=function.get('function')
			relations=self.get('relations').keys()
			if f in relations:
				operation=self[f]
				inputs,values=output
				for i in range(len(inputs)):
					k=inputs[i]
					x=values[i]
					if x==UNKNOWN:
						values[i]=k
				output=operation(*values)
			return output

	def __call__(self, *data):
		inputs=self.get('inputs')
		for i in range(len(inputs)):
			self[inputs[i]]=data[i]
		values=[]
		functions=self.get('process')
		for f in functions:
			values.append(self.execute(f))
		outputs=self.get('outputs')
		if outputs!=[]:
			values=self.retrieve(outputs)
		return values
