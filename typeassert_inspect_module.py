import inspect
import functools


def typeassert(*args,**kwargs):
	def decorate(func):
		sig = inspect.signature(func)
		bind_pars = sig.bind_partial(*args, **kwargs).arguments
		print(bind_pars)
		@functools.wraps(func)
		def wrapper(*fargs, **fkwargs):
			bind_values = sig.bind(*fargs, **fkwargs).arguments
			for key,value in bind_values.items():
				if key in bind_pars:
					if type(value)!=bind_pars[key]:
						raise TypeError("Expected {!r}= {!r} type".format(
							key, bind_pars[key].__name__))
			print("----------")
			for parameters,defaults in sig.parameters.items():
				if parameters not in bind_values:
					if type(defaults.default) != bind_pars[parameters]:
						raise TypeError("Expected {!r}= {!r} type".format(
							parameters, bind_pars[parameters].__name__))
			return func(*fargs, **kwargs)

		return wrapper
	return decorate

@typeassert(str, float, int)
def test(name, salary, age="22"):
	print(name)
	print(salary)
	print(age)
	pass

if __name__ == '__main__':
	r = test("meles", 30303.0,22)