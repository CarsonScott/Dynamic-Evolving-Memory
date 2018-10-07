from lib.base import *
from model import *

class Agent(Model):
	def __init__(self):
		super().__init__()
		self.meta=Model()
	def send_to(self, target, data):
		self[target].append(data)
		return self[target]
	def pull_from(self, target):
		return self[target].pop()
	def del_from(self, target, index):
		del self[target][index]
	def set_attribute(self, key, attribute, data):
		k=merge('-', [key, attribute])
		self.set_members(k, data)
	def get_attribute(self, key, attribute):
		k=merge('-', [key, attribute])
		return self.get_members(k)
	def size_of(self, target):
		return len(self[target])
	def type_of(self, target):
		return type(self[target])
	def is_empty(self, target):
		return self.size_of(target)==0
	def is_full(self, target):
		return self.size_of(target)==self.get_attribute(target, 'size')
	def is_class(self, name):
		return name in self.meta and is_type(self.get_members(name), list)
	def in_class(self, key, name):
		if self.is_class(name):
			return key in self.get_members(name)
	def define(self, name):
		self.set_members(name, [])
	def create(self, type, key, data):
		self.set_classes(key, type)
		self.assign(key, data)
	def set_classes(self, key, name):
		if is_type(name, list):
			for i in range(len(name)):
				ni=name[i]
				self.set_classes(key, ni)
		elif self.is_class(name):
			if not self.in_class(key, name):
				self.get_members(name).append(key)
	def get_classes(self, key):
		classes=[]
		for i in self.meta.keys():
			if self.in_class(key, i):
				classes.append(i)
		return classes
	def get_members(self, name):
		return self.meta[name]
	def set_members(self, name, members):
		self.meta[name]=members

# a=ComputerAgent()
# print(a.compute(['define', 'new_class']))
# print(a.compute(['create', 'new_class', 'x', 34]))
# print(a.compute(['create', 'functions', 'add', Object(['a', 'b'], {'function':add})]))
# print(a.compute(['add', 5, 6]))
# print(a.compute(['get', 'x']))
# print(a.compute(['define', 'c1']))
# print(a.compute(['set_classes', 'x', 'c1']))
# print(a.meta)
# print()

# a.create('expressions', 'e1', ['add', 45, 5])
# print(a.compute('e1'))

# print(a.meta['functions'])

