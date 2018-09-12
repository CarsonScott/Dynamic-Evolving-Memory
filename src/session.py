from formula import *
from utilities import merge
from generator import Generator
from lib.util import *
from saveload import *

gen=Generator(ignored=['|'])
expr=gen('(f(x y))')

def create_function(expression, memory=Dict(), root=True):
	if not root:data=expression
	else:data=gen(expression)
	X=[]
	for i in range(len(data)):
		x=data[i]
		if isinstance(x, list):
			if len(x)==2:
				x=create_function(x, memory, False)
			if len(x) == 1:
				x=x[0]
		if isinstance(x, str):
			if x in memory.keys():
				x=memory[x]
		X.append(x)
	Y=X
	if isinstance(Y, list):
		for i in range(len(Y)):
			if not isinstance(Y[i], Function):
				if isinstance(Y[i], list) and len(Y[i])==2:
					Y[i]=create_function(Y[i], memory, False)
				elif Y[i] in memory.keys():
					Y[i]=create_function(memory[Y[i]], memory, False)
		if len(Y)==1:
			if isinstance(Y[0], list):
				Y=create_function(Y[0], memory, False)
			elif not isinstance(Y[0], list):
				Y=create_function(Y[0], memory, False)
		if len(Y)==2:
			if isinstance(Y[1], list):
				f, v = Y
				if f in memory.keys():
					f=memory[f]
				if isinstance(v, list):
					for j in range(len(v)):
						if v[j] in memory.keys():
							v[j]=memory[v[j]]
				Y=Function(f, v, v)
	return Y
	
log=open('log.txt', 'w')
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
	def __init__(self, data=Dict()):
		super().__init__()
		self.assign('state', 0)
		self.assign('output', Dict())
		self.assign('active', list())
		self.assign('paths', Dict())
		self.assign('record', Dict())
		self.assign('history', Dict())
		self.assign('schedule', Dict())
		self.assign('progress', 0)
		self.assign('objective', rand_select)
		for i in data.keys():
			self[i]=data[i]

	def __call__(self):
		state=self.get('state')
		new_state=self.update()
		if new_state != state:
			output=self.get('output')
			if state not in output.keys():
				self['history'][state]=output
			
			output=Dict()
			active=self.activate(new_state)
			record=[i for i in range(len(active))]
			self.set('record', record)
			self.set('output', output)
		active=self.get('active')
		record=self.get('record')
		output=self.get('output')
		self.set('known', self.known)
		self.set('record', record)
		
		if len(record) > 0:
			index=rr(len(record))
			key=record[index]
			function=active[key]
			self.compute(function)
			progress=self.get('progress') + 1/len(output.keys())
			self.set('progress', progress)
			del record[index]
		else:self.set('progress', 1)

		self.set('output', output)
		history=self.get('history')
		return history

	def create(self, state, function):
		if state not in self.get('schedule').keys():
			self['schedule'][state]=list()
		self['schedule'][state].append(function)
		return function

	def activate(self, state):
		if state in self.get('schedule').keys():
			active=self['schedule'][state]
			self.set('active', active)
			self.set('progress', 0)
			return active
		else:
			self.set('progress', 1)
			return Dict()

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
			return Event(t, self.convert(b))
		
		elif isinstance(body, list):
			output=[]
			for i in range(len(body)):
				output.append(self.convert(body[i]))
			return output
		
		elif isinstance(body, str):
			output=self.translate(body)
			if output != None:
				return output
		return body

	def translate(self, keyword):
		if isinstance(keyword, str):
			if keyword not in self.keys():
				keyword=self.parse(keyword)
	
		if isinstance(keyword, list):
			if len(keyword)==2:
				f,X=keyword
				Y=[]
				for i in range(len(X)):
					if X[i] in self.keys():
						Y.append(self.translate(X[i]))

				return Function(f,Y,Y)
			elif len(keyword)==1:
				return keyword[0]
	
		elif isinstance(keyword, Function):
			f=keyword.get('function')
			X=keyword.get('inputs')
			return '(' + str(f) + '(' + merge(',', X) + '))'
		return keyword

	def compute(self, body):
		if isinstance(body, str):
			body=self.parse(body)
		if body in self.keys():
			body=self[body]

		if isinstance(body, str):
			key=body
			body=self.translate(body)
			data=self.convert(body)

		elif isinstance(body, list):
			body=self.translate(body)
			if isinstance(body, Dict):
				body=list(body.values())
			for i in range(len(body)):
				body[i]=self.translate(body[i])
			data=self.convert(body)
		
		elif isinstance(body, Function):
			key=self.translate(body)
			data=self.convert(body)
		
		if isinstance(data, list):
			return data
			data=self.convert(data)
			for i in range(len(data)):
				data[i]=self.convert(data[i])
				if isinstance(data[i], Function):
					data[i]=self.compute(data[i])
		if isinstance(data, list):
			data=self.compute(data)
		data=data()
		self['output'][key]=data
		return data

	def transfer(self):
		state=self.get('state')
		paths=self.get('paths')[state]
		options=paths.keys()
		data=[paths[i] for i in options]
		if callable(data[0]):
			X=[]
			for i in range(len(data)):
				y=self.compute(data[i])
				if y:X.append(y)
			data=X
		else:
			X=[]
			for i in range(len(data)):
				X=self.convert(data[i])
		objective=self.get('objective')

		if len(data) > 0:
			selection=objective(data)
			index=data.index(selection)
			return options[index]
		return state

	def update(self):
		if self.get('progress') == 1:
			state=self.transfer()
			self.set('state', state)
		return self.get('state')

	def parse(self, expression):
		return self.get('generator')(expression)

if __name__=="__main__":
	session=Session(function_list())
	size=20
	inputs=Dict()
	result=Dict()
	for i in range(size):
		if i == 0:inputs[i]=[0,0]
		else:
			inputs[i]=rand_list(2, [0,1])
		result[i]=UNKNOWN
		if i == size-1:session['paths'][i]=Dict({i-1:Function('LT', ['x','y'], ['x','y']), 0:Function('GT', ['x','y'], ['x','y'])})
		elif i == 0:session['paths'][i]=Dict({size-1:Function('LT', ['x', 'y'], ['x', 'y']), 1:Function('GT', ['x','y'], ['x','y'])})
		else:session['paths'][i] = Dict({rr(size):Function('LT', ['x', 'y'], ['x', 'y']), rr(size):Function('GT', ['x', 'y'], ['x','y'])})

	results=Dict()
	for rounds in range(200):
		lstate=session.get('state')
		session.set(['x', 'y'], rand_list(2, [0,1]))#inputs[lstate])
		Y=session()
		nstate=session.get('state')
		string=''
		for key in Y.keys():
			string += str(key) + ':\n'
			if isinstance(Y[key], Dict):
				F=Dict()
				for i in Y[key].keys():
					if Y[key][i] == True:
						F[i]=Y[key][i]
					string += '	' + str(i) + ' --> ' + str(Y[key][i]) + '\n'
				if key not in results.keys():
					results[key]=F
				else:results[key]=compound(results[key], F)
			else:
				string +='	' + str(Y[key]) + '\n'
		print(string)
	for i in results.keys():
		print(i, results[i])

	save(results, 'session_result.bin')