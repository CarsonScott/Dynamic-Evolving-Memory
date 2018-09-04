from lib.util import *

class Template(Dict):
	def __init__(self, keywords=[], functions=[]):
		self.func_list = []
		self.data_list = []
		self.expr_list = []
		for i in range(len(keywords)):
			k = keywords[i]
			f = functions[i]
			t = FUNC
			self.set(k,f,t)
		
	def __call__(self, data):
		output = Template()
		for i in self.func_list:
			v = self[i](data)
			t = DATA
			output.set(i,v,t)
		return output

	def set(self, key, value=UNKNOWN, type=None):
		if isinstance(key, list) or isinstance(key, tuple):
			for i in range(len(key)):
				k = key[i]
				if not isinstance(value, list) and not isinstance(value, tuple):
					v = value
				elif len(value) == len(key):
					v = value[i]
				else:v = None
				if not isinstance(type, list):
					t = type
				elif len(function) == len(key):
					t = type[i]
				else:t = DATA
				self.set(k,v,t)
		else:
			if key not in self.keys():
				if type==FUNC:
					self.func_list.append(key)
				elif type==DATA:
					self.data_list.append(key)
				elif type==EXPR:
					self.expr_list.append(key)
			self[key] = value

	def get(self, key):
		if key in self.keys():
			return self[key]
		return UNKNOWN

	def retrieve(self, key):
		output = UNKNOWN
		if key in self.keys():
			return self.retrieve(self[key])
		elif isinstance(key, list) or isinstance(key, tuple):
			output = []
			for i in range(len(key)):
				y = self.retrieve(key[i])
				output.append(y)
			if isinstance(key, tuple):
				output = tuple(output)
			return output
		else:return key