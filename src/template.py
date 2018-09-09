from lib.util import *

class Template(Dict):
	def __init__(self, *data):
		self.func_list = []
		self.data_list = []
		self.expr_list = []
		keywords=[]
		functions=[]
		if len(data)==1 and isinstance(data[0], Dict):
			keywords=data[0].keys()
			functions=list(data[0].values())
		elif len(data)==2 and eq_type(*data):
			if isinstance(data[0], list):
				keywords=data[0]
				functions=data[1]
		for i in range(len(keywords)):
			k = keywords[i]
			f = functions[i]
			t = FUNC
			self.set(k,f,t)
		
	def __call__(self, *data):
		output = Template()
		for i in self.func_list:
			if callable(self[i]):
				v = self[i](*data)	
			else:v = UNKNOWN
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
			key=self[key]
		if isinstance(key, list) or isinstance(key, tuple):
			output = []
			for i in range(len(key)):
				y = self.retrieve(key[i])
				output.append(y)
			if isinstance(key, tuple):
				output = tuple(output)
			return output
		else:return key

	def define(self, *data):
		if isinstance(data,list):
			if len(data) == 2:
				key,value=data
				print(key,value)
				if isinstance(key,list):
					for i in range(len(keys)):
						k=key[i]
						if isinstance(value,list):
							x=value[i]
						else:x=value
						self.set(k,x)
				else:self.set(key,value)
		elif isinstance(data, Dict):
			for i in data.keys():
				self.set(i, data[i])

	def functions(self):
		return self.func_list