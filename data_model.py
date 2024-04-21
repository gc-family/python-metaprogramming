class Descriptor:
    def __init__(self, name=None, **kwargs):
        self.name = '_' + str(name)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class TypeCheck(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise ValueError("Expected -> {}".format(self.expected_type.__name__))
        super(TypeCheck, self).__set__(instance, value)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected value is >= 0")
        super(Unsigned, self).__set__(instance, value)


class MaxSized(Descriptor):
    size = TypeCheck('size')
    size.expected_type = int

    def __init__(self, name=None, **kwargs):
        if 'size' not in kwargs:
            raise TypeError('missing size option')
        super(MaxSized, self).__init__(name, **kwargs)
        pass

    def __set__(self, instance, value):
        if len(value) > self.size:
            raise ValueError("Expected length is : < {}".format(self.size))
        super(MaxSized, self).__set__(instance, value)


class Integer(TypeCheck):
    expected_type = int


class String(TypeCheck):
    expected_type = str


class Float(TypeCheck):
    expected_type = float


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class SizedString(String, MaxSized):
    pass


def check_attributes(**kwargs):
    def decorator(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                key = '_' + str(key)
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls

    return decorator


class CheckedMeta(type):
    def __new__(cls, cls_name, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                key = '_' + str(key)
                value.name = key
        return type.__new__(cls, cls_name, bases, methods)


class StockDirect:
    # Specify constraints
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# example
@check_attributes(
    name=SizedString(size=10),
    shares=UnsignedInteger,
    price=UnsignedFloat
)
class StockDecorator:
    # Specify constraints
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# Example
class StockMeta(metaclass=CheckedMeta):
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == '__main__':
    r = StockDirect("Meles", 20, 101000.0)
    print(r.__dict__)

    r = StockDecorator("Meles", 21, 101000.0)
    print(r.__dict__)

    r = StockMeta("Meles", 22, 101000.0)
    print(r.__dict__)

    # import time
    # start = time.time()
    # _max = pow(2,20)
    # for i in range(_max):
    #     r = StockDirect("Meles", 20, 101000.0)
    
    # print("Elapsed time : {}".format(time.time()-start))