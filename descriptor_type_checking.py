class TypeChecking:
    def __init__(self, name, type_, default=str):
        self.name = '_' + name
        self.type_ = default if not type_ else type_

    def __get__(self, instance, owner):
        if not instance:
            return self
        else:
            # return instance[self.name]
            # return super(owner, instance).__getattribute__(self.name)
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type_):
            raise ValueError("Expected {} type".format(self.type_.__name__))
        else:
            # super(instance.__class__, instance).__setattr__(self.name, value)
            instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print("implementing the previous implementation of __delete__")
        del instance.__dict__[self.name]
        # super(instance.__class__, instance).__delattr__(self.managed_attribute)


def typeassert(**kwargs):
    def decorate(cls):
        for name, type_ in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, TypeChecking(name, type_))
        return cls

    return decorate


@typeassert(name=str, age=int, sallary=float)
class Test:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary


if __name__ == '__main__':
    result = Test("name", 100, 20304.0)
    print(result.__dict__)
    print(result.name)
