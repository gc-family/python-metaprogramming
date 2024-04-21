from functools import wraps, partial
from inspect import signature
import time
import logging

def partial(func, *args, **kwargs):
	def wrapper(*fargs, **fkwargs):
		newkwargs = {**kwargs, **fkwargs}
		return func(*args, *fargs, **newkwargs)

	wrapper.func = func
	wrapper.args = args
	wrapper.kwargs = kwargs
	return wrapper


def timethis(func=None, loop=1):
	"""decorator for time measure of function execution
		loop=integer value, - determine how many times the
		function invoked?
	"""
	if func is None:
		return partial(timethis,loop=loop)
	if loop <= 0:
		raise ValueError("Must be value of loop > 0")

	@wraps(func)
	def wrapper(*args, **kwargs):
		start = time.time()
		for _ in range(loop):
			result = func(*args, **kwargs)

		end = time.time()
		print('elapsed time : ----->{}-function'.format(func.__name__), end-start)
		return result
	return wrapper


def typeassert(*ty_args, **ty_kwargs):
	def decorate(func):
		if not __debug__:
			return func

		sig = signature(func)
		# bounding the func arguments and the given types ---ty_args,
		# and ty_kwargs
		bounded = sig.bind_partial(*ty_args, **ty_kwargs)
		bound_types = bounded.arguments

		@wraps(func)
		def wrapper(*args, **kwargs):
			bound_values = sig.bind(*args, **kwargs)
			for argument, value in bound_values.arguments.items():
				if argument in bound_types:
					if not isinstance(value, bound_types.get(argument)):
						raise TypeError('Argument {} must be {}'.format(argument, bound_types[argument].__name__))
			return func(*args, **kwargs)
		return wrapper
	return decorate






def attach_wrapper(obj, func=None):
	if func is None:
		return partial(attach_wrapper, obj)
	setattr(obj, func.__name__, func)


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):

	if func is None:
		return partial(logged, level=level, name=name, message=message)
	
	logname = name if name else func.__module__
	log = logging.getLogger(logname)
	logmsg = message if message else func.__name__
	
	if not __debug__:
		return func

	@wraps(func)
	def wrapper(*args, **kwargs):
		log.log(level, logmsg)
		return func(*args, **kwargs)


	@attach_wrapper(wrapper)
	def set_level(newlevel):
		nonlocal level
		level = newlevel

	@attach_wrapper(wrapper)
	def set_message(newlogmsg):
		nonlocal logmsg
		logmsg = newlogmsg

	@attach_wrapper(wrapper)
	def get_level():
		return level

	@attach_wrapper(wrapper)
	def get_message():
		return logmsg


	return wrapper

# -----------------------------------------tests-------------------------------------------------
# Example use
@timethis(loop=pow(2,10))
@typeassert(int, int)
@logged(level=logging.WARNING)
def add(x, y):
	return x + y

@logged(level=logging.CRITICAL, name='example')
def spam():
	print('Spam!')

@timethis(loop=1)
def time_test():
	return "tested"

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	if __debug__:
		add.set_message("Hell for war")
		print(add.get_message)
	r = add(120,30)
	s = spam()
	time_test()