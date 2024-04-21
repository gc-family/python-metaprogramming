
import inspect
from functools import wraps, partial


def typeassert(*type_args, **type_kwargs):
	def decorate(func):
		sig = inspect.signature(func)
		binded_types = sig.bind_partial(*type_args, **type_kwargs)

		for key, value in sig.parameters.items():
			if (value.default != value.empty) and (key in binded_types.arguments):
				if not isinstance(value.default, binded_types.arguments.get(key)):
					raise TypeError("Expected default value at function declaration of {!r} : {}".format(
												key, binded_types.arguments.get(key).__name__))

		@wraps(func)
		def wrapper(*args, **kwargs):
			binded_values = sig.bind(*args, **kwargs)
			for parm, value in binded_values.arguments.items():
				if parm in binded_types.arguments:
					if not isinstance(value, binded_types.arguments.get(parm)):
						raise TypeError("Expected : {}".format(binded_types.arguments.get(parm).__name__))
			return func(*args,**kwargs)

		return wrapper

	return decorate


@typeassert(str, age=int)
def test(name, salary, age=22):
	print(name,salary, age, sep='\n')

if __name__ == '__main__':
	r = test("Meles", 1000000.0)