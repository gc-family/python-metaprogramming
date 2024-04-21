class ClassMethodDescriptor(object):
    """docstring for ClassMethodDescriptor"""
    def __init__(self, class_method_):
        super(ClassMethodDescriptor, self).__init__()
        self.class_method_ = class_method_

    def __get__(self,instance,owner):
        return lambda *args : self.class_method_(owner)

    def __set__(self,instance,value):
        pass
        
    def __delete__(self,instance):
        pass


class StaticMethodDescriptor(object):
    """docstring for ClassMethodDescriptor"""
    def __init__(self, static_method_):
        super(StaticMethodDescriptor, self).__init__()
        self.static_method_ = static_method_

    def __get__(self,instance,owner):
       return self.static_method_

    def __set__(self,instance,value):
        pass
        
    def __delete__(self,instance):
        pass


class PropertryDescriptor(object):
    """docstring for PropertryDescriptor"""
    def __init__(self, fget=None, fset=None, fdel=None, fdoc=None):
        super(PropertryDescriptor, self).__init__()
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.fdoc = fdoc


    def __get__(self,instance,owner):
        print("get is invoked")
        if instance is not None:
            if self.fget:
                return self.fget(instance)
            else:
                raise AttributeError()
        else:
            return self


    def __set__(self,instance,value):
        if self.fset:
            return self.fset(instance,value)
        else:
            raise AttributeError("setting {} is not allowed".format(self.fget.__name__))

    def __delete__(self,instance):
        if self.fdel:
            return self.fdel(instance)
        else:
            raise AttributeError("deleting {} is not allowed".format(self.fget.__name__))

    def getter(self,_instance_method_):
        self.fget = _instance_method_
        return self

    def setter(self,_instance_method_):
        self.fset = _instance_method_
        return self


    def deleter(self, _instance_method_):
        self.fdel = _instance_method_
        return self


class Test(object):
    """docstring for Test"""
    age = 1000
    def __init__(self):
        super(Test, self).__init__()
        self.lists = [i for i in range(10)]

    def __getattr__(self,attr):
        print("{} is unknown attribute".format(attr))
        return getattr(str,attr)

    def __getitem__(self,index):
        return self.lists[index]

    def __getattribute__(self, attr):
        print("getting attribute : {}".format(attr))
        return super(Test,self).__getattribute__(attr)
    
    @PropertryDescriptor
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise ValueError("Must be String type")
        else:
            self._name = value

    @StaticMethodDescriptor
    def static_name():
        return Test.name

    @ClassMethodDescriptor
    def get_age(cls):
        return cls.age
    


class SubTest(Test):
    pass

if __name__ == '__main__':
    r = Test()
    r.name = "Meles Hailesselasie"
    print(Test.get_age(str))
    print(r.get_age())