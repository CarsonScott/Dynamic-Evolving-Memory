from formula import *

class Event(Model):
	def __init__(self, time=UNKNOWN, body=UNKNOWN):
		super().__init__()
		self.assign('time', time)
		self.assign('body', body)
	def __call__(self, *data):
		time=self.get('time')
		body=self.get('body')
		if len(data) > 0:
			time=data[0]
			if len(data)>=1:
				body=data[1]
		return time, body

class Session(Model):
	def __init__(self, delay=1, time=0):
		super().__init__()
		self.assign('delay', delay)
		self.assign('step', 0)
		self.assign('state', 0)
		self.assign('delta', 0)
		self.assign('delta', 0)
		self.assign('active', list())
		self.assign('record', Dict())

	def reset(self):
		record=self.get('record')
		active=self.get('active')
		for i in range(len(active)):
			time, body = active[i]()
			if time not in record.keys():
				record[time]=list()
			record[time].append(body)
		self.set('active', list())

	def time(self):
		step=self.get('step')
		delay=self.get('delay')
		if is_num(step) and is_num(delay):
			return step*delay

	def append(self, key, value):
		self[key].append(value)

	def access(self, key, index):
		return self[key][index]

	def create(self, event_body, event_time=None):
		if event_time==None:
			event_time=self.time()
		event=Event(event_time, event_body)
		if event_time not in self.get('record').keys():
			self['record'][event_time]=list()
		self['record'][event_time].append(event)
		return event

	def activate(self, time):
		if time in self.get('record').keys():
			active=self['record'][time]
		else:active=[]
		self.set('active', active)

	def convert(self, body):
		if body in self.keys():
			return self[body]

		elif isinstance(body, Function):
			func=Function(None, [], [], body)
			func['function']=self.convert(func['function'])
			interface=to_dict(func.get('interface'))
			for i in interface.keys():
				if interface[i]==UNKNOWN:
					func[i]=self.convert(i)
					interface[i]=func[i]
				func['interface']=[]
			return func
		elif isinstance(body, Formula):
			f=self.convert(body.get('function'))
			return Formula(f, body.get('arity'), body.get('constraints'))
		elif isinstance(body, Event):
			t,b = body()
			print(t,b)
			return Event(t, self.convert(b))
		elif isinstance(body, list):
			output=[]
			for i in range(len(body)):
				output.append(self.convert(body[i]))
			return output
		return body

	def compute(self):
		active=self.get('active')
		outputs=Dict()
		for i in range(len(active)):
			if isinstance(active[i], Event):
				time, body = active[i]()
				data = self.convert(body)
				key=(time, body['function'], *body['inputs'])
				value=data()
				outputs[key]=value
		return outputs

	def update(self, dt=None):
		delay=self.get('delay')
		delta=self.get('delta')
		if dt == None:
			dt = delay
		delta+=dt
		if delta >= delay:
			step=self.get('step')
			step+=1
			self.set('step', step)
			self.set('delta', 0)
			self.set('state', 1)
		else:
			self.set('state', 0)
			self.set('delta', delta)
		return self.get('state')
