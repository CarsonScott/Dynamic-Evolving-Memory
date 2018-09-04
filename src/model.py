from template import *

class Model(Template):
	def __init__(self, *data):
		super().__init__(*data)
		self.lock_list = []
		self.role_list = []

	def __call__(self):
		output=Template()
		for i in range(len(self.role_list)):
			key = self.role_list[i]
			value = self.get(key)
			output.set(key, value)
		return output

	def lock(self, key, constraint):
		self.lock_list.append(key)
		self[key] = Lock(self[key], constraint)

	def assign(self, role, data):
		self.role_list.append(role)
		self[role]=data

	def get(self, key, *data):
		if key in self.lock_list:
			return self[key](*data)
		return super().get(key)
