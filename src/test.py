from template_solver import *
from expression import *
from generator import *
from formula import *

class Experiment(Model):
	def __init__(self, events=[]):
		self.assign('count', 0)
		self.assign('pool', Pool(len(events), events))

def type_constraint(t):
	return Function(EQ, ['t','y'], ['x0'], {'t':t,'y':Function(TYPE,['x0'], ['x0'])})

def create_formula(data):
	if isinstance(data, Dict) and contains(data.keys(), ['arity', 'function', 'constraints']):
		a=data['arity']
		f=data['function']
		c=data['constraints']
		F=Formula(f,a)
		for i in data.keys():
			F.set(i, data[i])
		return F

def compose(data):
	if isinstance(data,list):
		output=[]
		for i in range(len(data)):
			output.append(compose(data[i]))
		return output
	elif isinstance(data,tuple):
		for i in range(len(data)-1):
			a=data[i]
			b=data[i+1]
			if isinstance(a, Dict) and isinstance(b, list):
				formula=create_formula(a)
				inputs=compose(b)
				function=formula(*inputs)
				return function
	else:return data

generator=Generator(open=[':'], close=['.'], accepted=['+', '*'], ignored=[',', '|'])
expression=generator('(+ (X (* (Y Z(+ (B C))))))')

print(expression)
context=Expression(*expression)

context['X']=1
context['Y']=2
context['Z']=3

context['A']=4
context['B']=5
context['C']=6

context['+']=Formula(sum)
context['*']=Formula(product)

model=context.retrieve(context.model())
function=compose(model)
print(function(), function)

Not=Formula(NOT,INF,{0:type_constraint(bool)})
And=Formula(AND,INF,{0:type_constraint(bool)})
Or=Formula(OR,INF,{0:type_constraint(bool)})
Set=Formula(SET,2,{0:type_constraint(Constant)})
Error=Formula(ERROR)
Equal=Formula(EQ)

FORMULAS=Dict({
	'error':Error,
	'equal':Equal,
	'set':Set,
	'not':Not,
	'and':And,
	'or':Or,
	})

def create(formula, *data):
	return FORMULAS[formula](*data)

equal_func = create('equal', 54, 54)
error_func = create('error', [1,0,0,1,0],[0,1,0,1,0],[1,1,0,1,0])
set_func = create('set', Constant('a'), 5)
and_func = create('and', True, True, True)
not_func = create('not', False, False)
or_func = create('or', True, False)

# print(error_func())
# print(equal_func())
# print(set_func())
# print(and_func())
# print(not_func())
# print(or_func())
# print(All(True,False,False,True)())
# f.set('x', Function(sum, ['a','b','c']))
# f.set('y', Function(pow, ('a','b')))
# # print(f(12,11,323))

# keywords = ['sum', 'product', 'average', 'gt', 'lt', 'eq']
# functions = [sum, product, average, GT, LT, EQ]
# template = Template()
# template.set(keywords, functions, FUNC)
# solver = TemplateSolver(template, 0.5, 0.4)

# data = [5, 2]
# goal = [True, 7, 10]

# objective = ['gt', 'sum', 'product']
# output = solver.update(data, goal)

# solution = solver()
# result = solution(data)
# model = Model(result.keys(), list(result.values()))
# score = solver.check()

# error = norm_error(objective, output)
# print('Functions:',keywords)
# print('Inputs:		', data)
# print('Valid:		', score)
# print('Goal:		', objective)
# print('Output:		', output)
# print('Error:		', error)
# print()
# print(solution)
# print(solution(data))

# model.lock('gt', GT)
# print([3,2], model.get('gt', [3,2]))
# print([2,3], model.get('gt', [2,3]))
# print([3,3], model.get('gt', [3,3]))