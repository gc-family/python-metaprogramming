from functools import wraps

class ClassMethod:
    def __init__(self,func):
        self.func = func

    def __get__(self,instance,owner):
        @wraps(self.func)
        def wrapper(*args,**kwargs):
            print(args)
            return self.func(owner)
        return wrapper

    def controler(self,instance,func):
        pass

    def __set__(self,instance,value):
        return self
        pass

    # def __delete__(self,instance):
    #     pass


class Test:
    @ClassMethod
    def name(cls):
        print("hello world")


if __name__ == '__main__':
    r = Test()
    r.name()
    Test.name()
    print(r.name)