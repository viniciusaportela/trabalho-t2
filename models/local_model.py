from models.address_model import Address


class Local:
    def __init__(self, name, cep, street, number, complement):
        self.__name = name
        self.__address = Address(cep, street, number, complement)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address: str):
        self.__address = address