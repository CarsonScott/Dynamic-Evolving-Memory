from schema import * 
from computer_agent import *

class Database(ComputerAgent):
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
						return
		else:super().__setitem__(key,value)

	def has_object(self, key):return self.in_class(key, 'objects')
	def set_object(self, key, value):self.create('objects', key, value)
	def get_object(self, key):return self[key] if self.has_object(key) else EMPTY
	def is_attribute(self, attribute):return self.in_class(attribute,'attributes')
	def has_attribute(self, key, attribute):return key in self[attribute]
	def set_attribute(self, key, attribute, value):self[attribute][key]=value
	def get_attribute(self, key, attribute):return self[attribute][key] if self.has_attribute(key,attribute) else EMPTY
	
	def is_relation(self, key, attribute):
		if self.has_attribute(key,attribute):
			value=self.get_attribute(key,attribute)
			if is_iter(value) or isinstance(value, Dict):
				return True
		return False

	def has_relation(self, source, attribute, target):
		if self.is_relation(source, attribute):
			value=self.get_attribute(source, attribute)
			return target in value
		return False

	def instantiate(self, *values):
		schema=self['schema']
		return schema(values)

	def transform_value_data(self, key):
		object=Model()
		for i in self[key].keys():
			object.assign(i, self[key][i])
		return object

	def transform_attribute_data(self, key):
		object=Model()
		attributes=self.get_members('attributes')
		for i in range(len(attributes)):
			attribute=attributes[i]
			value=self.get_attribute(key,attribute)
			object[attribute]=value
		return object

	def transform_relation_data(self, key):
		relations=Model()
		objects=self.get_members('objects')
		attributes=self.get_members('attributes')
		for i in range(len(attributes)):
			attribute=attributes[i]
			if self.is_relation(key,attribute):
				value=self.get_attribute(key,attribute)
				for j in range(len(objects)):
					object=objects[j]
					if self.has_relation(key,attribute,object):
						if object not in relations:
							relations.assign(object, attribute)
						elif isinstance(relations[object], str) and attribute != relations[object]:
							relations[object]=[relations[object], attribute]
						elif is_iter(relations[object]) and attribute not in relations[object]:
							relations[object].append(attribute)
		return relations

	def transform_object(self, key):
		data=Model()
		data.assign('object', self.transform_value_data(key))
		data.assign('attributes', self.transform_attribute_data(key))
		data.assign('relations', self.transform_relation_data(key))
		return data

	def transform(self):
		data=Model()
		objects=self.get_members('objects')
		for i in objects:
			xi=self.transform_object(i)
			data.assign(i,xi)
		return data

if __name__=="__main__":
	db=Database(['parents', 'children', 'score'], Schema(['string', str], ['integer', int]))
	db.set_object('object_1', db.instantiate('hello', 1))
	db.set_object('object_2', db.instantiate('goodbye', 0))
	db['object_1.parents']=['object_2']
	db['object_2.children']=['object_1']
	db['object_1.score']=1
	db['object_2.score']=1
	
	x=db.transform()
	for i in x.keys():
		print(i)
		for j in x[i].keys():
			print('	'+j+':	'+str(x[i][j]))

	# print('attributes:')
	# print('	', db.format('object_1'))
	# print('	', db.format('object_2'))

	# print('relations:')
	# print('	', db.transform('object_1'))
	# print('	', db.transform('object_2'))
	# print()
