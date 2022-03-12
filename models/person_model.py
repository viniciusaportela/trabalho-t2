from models.address_model import Address
from abc import ABC, abstractmethod

class Person(ABC):
    @abstractmethod
    def __init__(self, cpf, name, birthday, cep, street, number, complement):
        self.__cpf = cpf
        self.__name = name
        self.__birthday = birthday
        self.__address = Address(cep, street, number, complement)
    
    @property
    @abstractmethod
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    @abstractmethod
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    @abstractmethod
    def name(self):
        return self.__name
    
    @name.setter
    @abstractmethod
    def name(self, name: str):
        self.__name = name
    
    @property
    @abstractmethod
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    @abstractmethod
    def birthday(self, birthday: str):
        self.__birthday = birthday
    
    @property
    @abstractmethod
    def address(self):
        return self.__address
    
    @address.setter
    @abstractmethod
    def address(self, address: str):
        self.__address = address

