class MelesProperty:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel  # Save unbound methods
        self.__doc__ = doc  # or other callables

    def __get__(self, instance, instancetype=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("can't get attribute")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def setter(self,func):
        print("setter is setted to {!r} @{}".format(func.__name__,id(func)))
        self.fset = func
        return self

    def getter(self,func):
        print("getter is setted to {!r} @{}".format(func.__name__,id(func)))
        self.fget = self
        return self

    def deleter(self,func):
        print("deleter is setted to {!r} @{}".format(func.__name__,id(func)))
        self.fdel = func
        return self


class Person:
    def __init__(self,name):
        self._name = name

    @MelesProperty
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value

    @name.deleter
    def name(self):
        print("deleted")

if __name__ == '__main__':
    x = Person("Meles Hailesslasie")
    print(x.name)
    del x.name
