from database import *

def replace(expression, key, value):
	output=[]
	for i in range(len(expression)):
		data=expression[i]
		if isinstance(data, list):
			data=replace(data, key, value)
		elif data==key:
			data=value
		output.append(data)
	return output

class EnergyAgent(Database):
	def __init__(self, filter, threshold=0, cost=0.5, inputs=9):
		schema=Schema(dimension('energy', int))
		attributes=['cost']
		super().__init__(attributes,schema)
		self.define('inputs')
		self.define('outputs')
		self.define('origin')
		for i in range(inputs):
			self.set_object('sensor_'+str(i), self.instantiate(0))
			self.create(['inputs', 'objects'], 'sensor_'+str(i), 0)
			self.create('outputs', 'motor_'+str(i), 0)
			self.set_attribute('sensor_'+str(i), 'cost', 1)
		self.set_members('origin', ['sensor_0', 'motor_0'])
		self.create('expressions', 'filter', filter)
		self.assign('threshold', threshold)
		self.assign('energy', 0)

	def update(self, inputs):
		objects=[]
		for i in range(len(inputs)):
			key='sensor_'+str(i)
			val=inputs[i]
			obj=self.instantiate(val)
			self.set_object(key, obj)
			objects.append(obj)
		return objects
	
	def filter(self, objects):
		options=[]
		function=self['filter']
		for i in range(len(objects)):
			object=objects[i]
			data=object['energy']
			key='sensor_'+str(i)
			fi=replace(function, UNKNOWN, data)
			yi=self.compute(fi)
			if yi:options.append(key)
		return options

	def rank(self, options):
		costs=[]
		for i in options:
			cost=self.get_attribute(i, 'cost')
			costs.append(cost)
		ranks=sort(costs)
		return [options[i] for i in ranks]

	def __call__(self, inputs):
		objects=self.update(inputs)
		options=self.filter(objects)
		options=self.rank(options)

if __name__=="__main__":
	agent=EnergyAgent(['or', ['gt', UNKNOWN, 1], ['eq', UNKNOWN, 1]])
	agent.create('functions', 'eq', Object(['x', 'y'], {'function':eq}))
	agent.create('functions', 'gt', Object(['x', 'y'], {'function':gt}))
	agent.create('functions', 'lt', Object(['x', 'y'], {'function':lt}))

	# print(agent['filter'](1))
	agent([rr(-10, 10) for i in range(9)])