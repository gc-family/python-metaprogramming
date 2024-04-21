


class Tracer:
	""""
		1, Decorated functions invoke only its __call__, and never invoke its __get__.
		2, Decorated methods invoke its __get__ first to resolve the method name fetch (on
			I.method); the object returned by __get__ retains the subject class instance and is
			then invoked to complete the call expression, thereby triggering the decorator’s
			__call__ (on ()).
	"""
	def __init__(self, func):
		self.func = func
		self.calls = 0

	def __get__(self, instance, owner):
		print('get is accessed')
		return Wrapper(self, instance)

	def __call__(self, *args, **kwargs):
		self.calls += 1
		print("calls %s to %s" % (self.calls, self.func.__name__))
		return self.func(*args, **kwargs)


class Wrapper:
	def __init__(self, decorator, instance):
		self.decorator = decorator
		self.instance = instance

	def __call__(self, *args, **kwargs):
		print("call function is invoked from wrapper")
		return self.decorator(self.instance, *args, **kwargs) #invoke Tracer.__call__


@Tracer
def spam(a, b, c):  # spam = tracer(spam)
	print(a,b,c)


class Person:

	def giveRaise(self, percent):  # giveRaise = tracer(giveRaise)
		pass
	giveRaise = Tracer(giveRaise)

if __name__ == '__main__':
	r = Person()
	r.giveRaise(10)