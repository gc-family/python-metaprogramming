class LasyProperty:
		""""
				this is the decorator of method in class
				Example:
						@LasyProperty
						def name(self):
								:return self._name
				"""
		def __init__(self,func):
				self.func = func

		def __get__(self, instance, owner):
				if not instance:
						return self
				else:
						value = self.func(instance)
						# instance.__class__.__setattr__(instance, '_' + self.func.__name__, value)
						setattr(instance, '_' + self.func.__name__, value)
						# instance.__setattr__('_' + self.func.__name__, value)
						return value

		@staticmethod
		def setter(func,*args,**kwargs):
				print(func.__name__)
				print(*args,**kwargs)

		def __set__(self, instance, value):
				raise ValueError("Read Only Attribute")

		def __delete__(self, instance):
				raise AttributeError("Cannot delete Attribute with name {}".format(self.func.__name__))

import math
class Circle:
		def __init__(self, radius):
				self.radius = radius

		@LasyProperty
		def area(self):
				print('Computing area')
				return math.pi * self.radius ** 2

		@LasyProperty
		def perimeter(self):
				print('Computing perimeter')
				return 2 * math.pi * self.radius

if __name__ == '__main__':
		c = Circle(radius=10)
		print(c.area)
		# this will show
		print(c.perimeter)
		print(c.__dict__)