from functools import *
from itertools import *


#  Simplifying the Initialization of Data Structures
class Structure:
	_fields = []
	def __init__(self, *args, **kwargs):
		if len(args) > len(self._fields):
			raise TypeError("Expected {} arguments".format(len(self._fields)))

		for name, value in zip(self._fields,args):
			setattr(self, name,value)

		# Set the remaining keyword arguments
		print(self._fields[len(args):])
		for name in self._fields[len(args):] :
			try:
				r = kwargs.pop(name)
			except Exception as e:
				raise TypeError("__init__() got an unexpected keyword argument {!r}".format(name))
			else:
				print("setting")
				setattr(self, name, r)

		# Set the additional arguments (if any)
		extra_args = kwargs.keys() - set(self._fields)
		for name in extra_args:
			setattr(self, name, kwargs.pop(name))

		# Check for any remaining unknown arguments
		if kwargs:
			raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))


	def __setattr__(self, key, value):
		print("Setting Attribute : '{1}' to {0}".format(key, value))
		return super(Structure, self).__setattr__(key, value)

class Test(Structure):
	_fields = ['name','age','salary']

if __name__ == '__main__':
	r = Test(
		"Meles",
		21,
		salary=1000.0,
		date='8/2/2012'
	)