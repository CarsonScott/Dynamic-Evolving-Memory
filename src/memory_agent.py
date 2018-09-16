from computer_agent import *

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
			self.set_capacity('memory', memory_size)

	# Determine validity of syntax of expression.
	def is_valid(self, expression):
		if is_type(expression, tuple):
			for i in range(len(expression)):
				ei=expression[i]
				if not self.is_valid(ei):
					return False
			return True
		return super().is_valid(expression)

	# Record expression and compute results.
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

	# Convert expression into sentence
	def encode(self, expression):
		words=combine_elements(expression)
		sentence=merge(' ', words)
		return sentence

	# Combine words into sentence and store in buffer.
	def update_buffer(self, expression):
		sentence=self.encode(expression)
		self.send_to('buffer', sentence)
		return sentence

	# Combine sentences into phrase and store in memory. 
	def update_memory(self):
		words=self['buffer']
		sentences=combine_elements(words)
		phrase=merge(', ', sentences) 
		if self.is_full('memory'):
			self.del_from('memory', 0)
		self.send_to('memory', phrase)
		self['buffer']=[]
		return self['memory']

	# Associated phrases with results and store in output.
	def update_output(self, data):
		buffer=self['buffer']
		output=combine_rows(buffer, data)
		self['output']=[]
		for i in range(len(output)):
			yi=output[i]
			yi=Translation(*yi)
			self.send_to('output', yi)
		return self['output']

	# Compute phrase-sequence and update mutable storage
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

	# determine options that satisfy constraint
	def select(self, *data):
		constraint=data[0]
		options=data[1:][0]
		data=[self[i] for i in options if i in self]
		if constraint in self: 
			function=self[constraint] 
		else:function=constraint
		indices=filter(function, *data)
		outputs=[]
		for i in indices:
			oi=options[i]
			outputs.append(oi)
		return outputs	
