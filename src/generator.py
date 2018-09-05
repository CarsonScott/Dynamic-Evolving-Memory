from lib.util import *

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-._'
OPEN = ['(']
CLOSE = [')']
CHARS = list(CHARS + CHARS.upper())
SPACES = list('	 ')

class Generator(list):
	def __init__(self, open=[], close=[], accepted=[], ignored=[]):
		self.accepted = union(CHARS, accepted)
		self.ignored = union(SPACES, ignored)
		self.leaf = True
		self.done = False
		self.open = union(OPEN, open)
		self.close = union(CLOSE, close)

	def __call__(self, expression):
		self.test(expression)
		output = []
		for c in expression:
			output = self.update(c)
		if len(output) == 1 and isinstance(output[0], Generator):
			output = output[0]
		return list(output)

	def test(self, expression):
		state = 0
		for c in expression:
			if c in self.open:
				state += 1
			elif c in self.close:
				state -= 1
			elif c not in self.accepted and c not in self.ignored:
				raise Exception(c + ' is not a valid character.')
		if state != 0:
			raise Exception(expression + ' is not a valid expression.')

	def update(self, c, root=True):
		if not self.done:
			if self.leaf:
				if c in self.open:
					gen = Generator(self.open, self.close, self.accepted, self.ignored)
					if len(self) > 0 and self[len(self)-1] == '':
						self[len(self)-1] = gen
					else:self.append(gen)
					self.leaf = False
				elif c in self.close:
					self.done = True
				elif c in self.accepted:
					if len(self) == 0 or not isinstance(self[len(self)-1], str):
						self.append(c)
					else:self[len(self)-1] += c
				elif c not in self.ignored:
					self.append(c)
				elif len(self) == 0 or self[len(self)-1] != '':
					self.append('')
			else:
				x = self[len(self)-1]
				if isinstance(x, Generator):
					if c == self.close and x.leaf == True:
						self[len(self)-1].done = True
						self.leaf = True
					self[len(self)-1].update(c, root=False)
		if self.done:
			while '' in self:
				del self[self.index('')]
		return self