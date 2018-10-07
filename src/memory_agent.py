from computer_agent import *

class Trajectory(Object):
	def __init__(self, initial=EMPTY, terminal=EMPTY):
		inputs=list()
		data=Dict()
		if initial==EMPTY:inputs.append('initial')
		else:data['initial']=initial
		if terminal==EMPTY:inputs.append('terminal')
		else:data['terminal']=terminal
		super().__init__(['initial', 'terminal'], data)

class MemoryAgent(ComputerAgent):
	def __init__(self, memory_size=UNKNOWN):
		super().__init__()
		self.define('inputs')
		self.define('main')
		self.define('mutable')
		self.create('mutable', 'memory', [])
		self.create('mutable', 'buffer', [])
		self.create('mutable', 'output', [])
		if memory_size!=UNKNOWN:
			self.set_attribute('memory', 'size', memory_size)

	# Determine validity of syntactic expression/expression block
	def is_valid(self, expression):
		if is_type(expression, tuple):
			for i in range(len(expression)):
				ei=expression[i]
				if not self.is_valid(ei):
					return False
			return True
		return super().is_valid(expression)

	# Record/convert expression into function and compute output
	def compute(self, expression, root=True):
		if is_type(expression, str):
			if self.in_class(expression, 'expressions'):
				expression=self.get(expression)
		if root:self.update_buffer(expression)
		if is_type(expression, tuple):
			outputs=[]
			for i in range(len(expression)):
				ei=expression[i]
				yi=self.compute(ei, root=False)
				outputs.append(yi)
			return outputs
		else:return super().compute(expression)

	# Combine words into sentence and store in buffer
	def update_buffer(self, expression):
		sentence=self.encode(expression)
		self.send_to('buffer', sentence)
		return sentence

	# Combine sentences into phrase and store in memory
	def update_memory(self):
		words=self['buffer']
		sentences=combine_elements(words)
		phrase=merge(', ', sentences) 
		if self.is_full('memory'):
			self.del_from('memory', 0)
		self.send_to('memory', phrase)
		self['buffer']=[]
		return self['memory']

	# Combine phrases with outputs and store in output 
	def update_output(self, data):
		buffer=self['buffer']
		output=combine_rows(buffer, data)
		self['output']=[]
		for i in range(len(output)):
			yi=output[i]
			yi=Trajectory(*yi)
			self.send_to('output', yi)
		return self['output']

	# Compute expression sequence and update storage
	def update(self, *data):
		inputs=self.meta['inputs']
		for i in range(len(data)):
			xi=data[i]
			ki=inputs[i]
			self[ki]=xi
		outputs=[]
		functions=self.meta['main']
		for i in functions:
			expression=self[i]
			output=self.compute(expression)
			if output==None:
				output=EMPTY
			outputs.append(output)
		output=self.update_output(outputs)
		memory=self.update_memory()
		return output
