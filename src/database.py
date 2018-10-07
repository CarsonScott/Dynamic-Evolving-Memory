from schema import * 

class Database(Agent):

	def __init__(self, attributes=list(), schema=Schema()):
		super().__init__()
		self.define('attributes')
		self.define('objects')
		for i in range(len(attributes)):
			self.create('attributes', attributes[i], Model())
		self.assign('schema', schema)
	
	def __getitem__(self, key):
		if '.' in key:
			if len(key.split('.'))==2:
				key,attribute=key.split('.')
				if self.has_object(key):
					if self.is_attribute(attribute):
						return self.get_attribute(key,attribute)
		return super().__getitem__(key)
	
	def __setitem__(self, key, value):
		if '.' in key:
			if len(key.split('.'))==2:
				key,attribute=key.split('.')
				if self.has_object(key):
					if self.is_attribute(attribute):
						self.set_attribute(key,attribute,value)
		super().__setitem__(key,value)

	def has_object(self, key):return key in self
	def set_object(self, key, value):self.create('objects', key, value)
	def get_object(self, key):return self[key] if self.has_object(key) else EMPTY
	def is_attribute(self, attribute):return self.in_class(attribute,'attributes')
	def has_attribute(self, key, attribute):return key in self[attribute]
	def set_attribute(self, key, attribute, value):self[attribute][key]=value
	def get_attribute(self, key, attribute):return self[attribute][key] if self.has_attribute(key,attribute) else EMPTY
	
	def is_relation(self, key, attribute):
		if self.has_attribute(key,attribute):
			value=self.get_attribute(key,attribute)
			if is_iter(value) or is_dict(value):
				return True
		return False
	def has_relation(self, source, attribute, target):
		if self.is_relation(source, attribute):
			value=self.get_attribute(source, attribute)
			return target in value
		return False

	def initialize(self, *values):
		schema=self['schema']
		return schema(values)

	def convert(self, key):
		object=Model()
		object.assign('key',key)
		attributes=self.get_members('attributes')
		for i in range(len(attributes)):
			attribute=attributes[i]
			value=self.get_attribute(key,attribute)
			object[attribute]=value
		return object

	def transform(self, key):
		structure=Agent()
		structure.assign('key', key)
		structure.define('neighbors')
		objects=self.get_members('objects')
		attributes=self.get_members('attributes')
		for i in range(len(attributes)):
			attribute=attributes[i]
			
			if self.is_relation(key,attribute):
				value=self.get_attribute(key,attribute)
				for j in range(len(objects)):
					object=objects[j]
					if self.has_relation(key,attribute,object):
						if not structure.in_class('neighbors', object):
							structure.create('neighbors', object, [attribute])
						elif attribute not in structure[object]:
							structure.send_to(object, attribute)
		return structure

if __name__=="__main__":

	db=Database(['parents', 'children'], Schema(['key', str], ['value', int]))

	db.set_object('object_1', db.initialize('hello', 1))
	db.set_object('object_2', db.initialize('goodbye', 0))

	db['object_1.parents']=['object_2']
	db['object_2.children']=['object_1']

	print('attributes:')
	print('	', db.convert('object_1'))
	print('	', db.convert('object_2'))

	print('relations:')
	print('	', db.transform('object_1'))
	print('	', db.transform('object_2'))
	print()
