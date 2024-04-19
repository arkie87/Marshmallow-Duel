class Collection:
    Collection = []

    def __init__(self):
        self.__class__.Collection += [self]

    def __repr__(self):
        return self.__class__.__name__


class StaticObject(Collection):
    Collection = []


class DynamicObject(Collection):
    Collection = []

    def __init__(self, v):
        super().__init__()
        self.v = v

    def __repr__(self):
        return super().__repr__() + f"({self.v})"


if __name__ == "__main__":
    c = Collection()
    Collection()
    Collection()

    s = StaticObject()
    StaticObject()
    StaticObject()
    StaticObject()

    d = DynamicObject(2)
    DynamicObject(1)
    DynamicObject(4)
    DynamicObject(10)
    DynamicObject(44)

    print(c.Collection)
    print(s.Collection)
    print(d.Collection)
