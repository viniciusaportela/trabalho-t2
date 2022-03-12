from models.person_model import Person


class Organizer(Person):
    def __init__(self, cpf, name, birthday, cep, street, number, complement):
        super().__init__(cpf, name, birthday, cep, street, number, complement)

    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
    
    @property
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    def birthday(self, birthday: str):
        self.__birthday = birthday
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address: str):
        self.__address = address