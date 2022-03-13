class Address:
    def __init__(self, cep, street, number, complement):
        self.__cep = cep
        self.__street = street
        self.__number = number
        self.__complement = complement

    def to_raw_str(self):
        return (
            self.street +
            ', n ' +
            self.number +
            ((', ' + self.complement) if self.complement != '' else '') +
            ' (' +
            self.cep +
            ')'
        )

    def to_raw(self):
        return {
            "cep": self.cep,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
        }

    @property
    def cep(self):
        return self.__cep

    @cep.setter
    def cep(self, cep: str):
        self.__cep = cep

    @property
    def street(self):
        return self.__street

    @street.setter
    def street(self, street: str):
        self.__street = street

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number: str):
        self.__number = number

    @property
    def complement(self):
        return self.__complement

    @complement.setter
    def complement(self, complement: str):
        self.__complement = complement
