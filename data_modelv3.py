class Descriptor(object):
    """docstring for Descriptor"""

    def __init__(self, name=None, **kwargs):
        super(Descriptor, self).__init__()
        self.name = "_" + str(name)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __get__(self, instance, owner):
        # print("__get__ is invoked")
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# descriptor for enforcing types

class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("Expected {!r}: {} type".format(self.name,
                                                            self.expected_type.__name__))

        super().__set__(instance, value)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >=0")
        super().__set__(instance, value)


class LimitedInteger(Descriptor):
    def __init__(self, name=None, max_size=pow(2, 10), **kwargs):
        kwargs['max_size'] = max_size
        super().__init__(name, **kwargs)

    def __set__(self, instance, value):
        if value > self.max_size:
            raise ValueError("Expected value of {!r} < {}".format(self.name[1:], self.max_size))
        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, size=48, **kwargs):
        kwargs['size'] = size
        super().__init__(name, **kwargs)
        pass

    def __set__(self, instance, value):
        if len(value) > self.size:
            raise ValueError('size of <-{}-> must be < '.format(self.name[1:]) + str(self.size))
        super().__set__(instance, value)


class String(Typed):
    expected_type = str


class Float(Typed):
    expected_type = float


class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class SizedString(String, MaxSized):
    size = UnsignedInteger('size')
    pass


class LimitedUnsignedInteger(Integer, Unsigned, LimitedInteger):
    pass


def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = "_" + str(key)
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls

    return decorate


# A metaclass that applies checking
class CheckedMeta(type):
    def __new__(mcs, cls_name, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = '_' + key
        return type.__new__(mcs, cls_name, bases, methods)


# ----------------test area--------------
@check_attributes(
    name=SizedString(size=20),
    age=LimitedUnsignedInteger(max_size=81)
)
class Test:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Stock(metaclass=CheckedMeta):
    name = SizedString(size=20)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == '__main__':
    r = Test("Meles Hailesselasie", age=pow(2, 3))
    r2 = Stock(name="meles haile", shares=20, price=pow(2, 10) / 1)
