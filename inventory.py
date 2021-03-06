class Inventory:
    def __init__(self, id=0, name='', type='', capacity=0, stock=0):
        self._id = id
        self._name = name
        self._type = type
        self._capacity = capacity
        self._stock = stock

    @staticmethod
    def parse_raw(row):
        if row is None or len(row) != 5:
            return Inventory()

        tempinventory = Inventory()
        tempinventory.id = row[0]
        tempinventory.name = row[1]
        tempinventory.type = row[2]
        tempinventory.capacity = row[3]
        tempinventory.stock = row[4]
        return tempinventory

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value
