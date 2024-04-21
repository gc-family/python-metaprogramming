# class decorator approach can also be used as a replacement for mixin
# classes, multiple inheritance, and tricky use of the super() function. Here is an alter‐
# native formulation of this recipe that uses class decorators:

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


# Decorator for applying type checking
def Typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expected_type, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('expected ' + str(expected_type))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


def MaxSized(cls):
    super_init = cls.__init__

    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super_init(self, name, **opts)

    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Specialized descriptors
@Typed(int)
class Integer(Descriptor):
    pass
@Unsigned
class UnsignedInteger(Integer):
    pass
@Typed(float)
class Float(Descriptor):
    pass
@Unsigned
class UnsignedFloat(Float):
    pass
@Typed(str)
class String(Descriptor):
    pass
@MaxSized
class SizedString(String):
    pass

class Test:
    name = SizedString(size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat("price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

if __name__ == '__main__':
    r = Test("Meles", 22, 101000.0)
    print(r.__dict__)

    # import time
    #
    # start = time.time()
    # _max = pow(2, 20)
    # for i in range(_max):
    #     r = Test("Meles", 20, 101000.0)
    #
    # print("Elapsed time : {}".format(time.time() - start))