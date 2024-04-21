def dictPrinter(dictionary):
	for i, (key, value) in enumerate(dictionary.items()):
		print(str(i), ',', key, '==', value)
	return None


class Ancestor:
	pass


class Test(Ancestor):
	pass


class TypedProperty(object):
	def __init__(self, name, types, default=None):
		self.name = '_' + name
		# self.name =  name
		self.types = types
		self.default = default if default else types()

	def __get__(self, instance, owner):
		print("Instance : ", instance, ">>>Class :", owner)
		return getattr(instance, self.name, self.default)

	def __set__(self, instance, value):
		print("this is the instance", instance)
		if not isinstance(value, self.types):
			raise TypeError("Must be a %s" % self.types)
		setattr(instance, self.name, value)

	def __delete__(self, instance):
		raise AttributeError("Can't delete attribute")

	def __str__(self):
		pass


class Foo(Test):
	num = TypedProperty("num", int, 42)
	name = TypedProperty("name", str)

	def update(self):
		pass

	def show(self):
		pass

	def delete(self):
		pass


class Foo(object):
	def spam(self, a, b):
		pass


class FooProxy(object):
	def __init__(self, f):
		self.f = f

	def spam(self, a, b):
		return self.f.spam(a, b)


class_name = "Foo" # Name of class
class_parents = (object,) # Base classes
class_body = """ # Class body
def __init__(self,x):
	self.x = x
def blah(self):
	print("Hello World")
"""
class_dict = { }
# Execute the body in the local dictionary class_dict
exec(class_body,globals(),class_dict)
# Create the class object Foo
Foo = type(class_name,class_parents,class_dict)

print(Foo)
print(type(Foo))