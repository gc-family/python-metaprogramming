import inspect
from typing import Any
from colorama import Fore, init
from functools import partial, wraps


init()
class _IntFloat(tuple):
	def __str__(self):
		return "int or float"
	
class MetaClass(type):
	"""docstring for MetaClass."""
	def __init__(self, clsname, bases, attributedict, **kwargs):
		super(MetaClass, self).__init__(clsname, bases, attributedict)
		self._clsname = clsname
		self._bases = bases
		self._attributedict = attributedict

	def __new__(cls, clsname, bases, attributedict, **kwargs):
		return super().__new__(cls, clsname, bases, attributedict)

	@classmethod
	def __prepare__(self, bases, attributedict, **kwargs):
		return dict()
	

	
class Descriptor(object):
	"""docstring for Descriptor."""
	def __init__(self, name):
		super(Descriptor, self).__init__()
		self.name = "_" + name

	def __get__(self, instance, owner):
		if not instance:
			return self
		return getattr(instance, self.name)
	
	def __set__(self, instance, value):
		return setattr(instance, self.name, value)

class DataType(Descriptor):
	_expected_type = None
	def __set__(self, instance, value):
		if not isinstance(value, self._expected_type):
			raise TypeError("Expected type is for {} is {}, but given is {} \
									 ".format(self.name, self._expected_type, type(value).__name__))
		return super().__set__(instance, value)

class StringType(DataType):
	_expected_type = str

class NumericType(DataType):
	_expected_type = _IntFloat([int, float])

class IntegerType(DataType):
	_expected_type = int

class FloatType(DataType):
	_expected_type = float

def cls_decorate(**kwargs):
	def wrapper(cls):
		for key, value in kwargs.items():
			assert(isinstance(key, str))
			if isinstance(value, Descriptor):
				setattr(cls, key, value)
			elif issubclass(value, Descriptor):
				setattr(cls, key, value(key))
			else:
				raise ValueError("Invalid Value for - '{}' attributes".format(key))
		return cls
	return wrapper


class Printer(object):
	def __init__(self):
		self._color = None

	def print_colored(self, *args, **kwargs):
		return print(self._color, *args, Fore.RESET, **kwargs)
	
	def __getattr__(self, attr:str):
		_start = "print_"
		if attr.startswith(_start):
			self._color = getattr(Fore, attr[len(_start):].upper())
		return self.print_colored
	
	def __call__(self, *args: Any, **kwargs: dict) -> Any:
		if "color" in kwargs:
			self._color = getattr(Fore, kwargs['color'].upper())
			kwargs.pop('color')
		else:
			self._color = getattr(Fore, "YELLOW")
		return self.print_colored(*args, **kwargs)

@cls_decorate(price=NumericType, fname=StringType, category=StringType)
class Item(metaclass=MetaClass):
	"""docstring for Item."""
	def __init__(self, fname, price, category):
		super(Item, self).__init__()
		self.fname = fname
		self.price = price
		self.category = category
	def __str__(self):
		return "Item - {}".format(self.fname)
	
	def __repr__(self):
		return "<Item - price={0.price}, name={0.fname}>".format(self)
	
	def test(self, arg):
		pass


import socket


class LazyConnection:
	def __init__(self, address, family=socket.AF_INET, type=socket.SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.sock = None

	def __enter__(self):
		if self.sock is not None:
			raise RuntimeError("Already Connected")
		self.sock = socket.socket(self.family, self.type, 0)
		self.sock.connect(self.address)
		return self.sock
	
	def __exit__(self, exc_ty, exc_val, tb):
		self.sock.close()
		self.sock = None


if __name__ == '__main__':
	Print = Printer()
	# # clothes = Item(name=, price="234", category="Closes")
	# clothes = Item(fname="T-shirt", price=123, category="Closes")
	# Print(clothes.fname, color="red")
	# Print(clothes.price, color="green")
	# Print(clothes.category, color="blue")
	# help("FORMATTING")
with LazyConnection(('localhost', 80)) as s:
	# conn.__enter__() executes: connection open
	s.send(b'GET /js/Modern%20javascript/ HTTP/1.0\r\n')
	s.send(b'Host: www.python.org\r\n')
	s.send(b'\r\n')
	resp = b''.join(iter(partial(s.recv, 8192), b''))
	# print(resp.decode())
import sys
class Date:
	# __slots__ = ['year', 'month', 'day']
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day

x = Date(1,2,3)
print(sys.getsizeof(x))