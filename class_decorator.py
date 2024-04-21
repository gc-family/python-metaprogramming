def singleton(a_class):  # On @ decoration
    instances = None

    def onCall(*args, **kwargs):  # On instance creation
        nonlocal instances
        if a_class is not None:  # One dict entry per class
            instances = a_class(*args, **kwargs)
        return instances

    return onCall


class SingleTon:
    def __init__(self, a_class):
        self.aClass = a_class
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.aClass(*args, **kwargs)
        return self.instance

class SingleTonV2:
    def __init__(self,a_class):
        self.a_class = a_class
        self.instance = None

    def __getattr__(self, item):
        return getattr(self.a_class,item)

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self._instantiate(*args, **kwargs)
        return self.instance

    def _instantiate(self,*args, **kwargs):
        setattr(self.a_class,"_singleTon","this is singleton pattern")
        return self.a_class(*args, **kwargs)

def singletonv3(a_class):
    class Wrapper:
        def __init__(self):
            self.a_class = a_class
            self.instance = None
            print("hello world")

        def __getattr__(self, item):
            return getattr(self.a_class,item)

        def __call__(self, *args, **kwargs):
            if self.instance is None:
                self.instance = self._instantiate(*args, **kwargs)
            return self.instance

        def _instantiate(self,*args, **kwargs):
            setattr(self.a_class,"_singleTon","this is singleton pattern")
            return self.a_class(*args, **kwargs)
    return Wrapper()


@singletonv3  # Person = singleton(Person)
class Person:  # Rebinds Person to onCall
    def __init__(self, name, hours, rate):  # onCall remembers Person
        self.name = name
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate


@singleton  # Spam = singleton(Spam)
class Spam:  # Rebinds Spam to onCall
    def __init__(self, val):  # onCall remembers Spam
        self.attr = val


if __name__ == '__main__':
    bob = Person('Bob', 40, 10)  # Really calls onCall
    sue = Person('Sue', 50, 20)  # Same, single object
    print(bob)
    print(dir(bob))
    print(bob._singleTon)
    print(Person._singleTon)
