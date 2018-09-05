from model import *

class Expression(Model):
	def __init__(self, connective, symbols):
		super().__init__()
		self.assign('relation', connective)
		self.assign('variables', symbols)
		self.assign('function', None)
		self.assign('sequence', None)

	def model(self, variables=None):
		sequence=self.get('sequence')
		function=self.get('function')
		relation=self.get('relation')
		if variables==None:
			variables=self.get('variables')
		submodels=[]
		for i in range(len(variables)):
			v=variables[i]
			if isinstance(v,list) or isinstance(v,tuple):
				if len(v)==2:
					variables[i]=Expression(*v)
				submodels.append(variables[i].model())
			else:submodels.append(v)
		models=[]	
		if function==None:
			function=[relation, [submodels[i] for i in range(len(submodels))]]
			self.set('function', function)
		return tuple(function)
		return model