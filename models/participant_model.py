from models.address_model import Address
from models.person_model import Person
from models.pcr_exam_model import PCRExam


class Participant(Person):
    # TODO don't repeat Abstract properties
    def __init__(self, cpf, name, birthday, cep, street, number, complement, has_two_vaccines=None, has_covid=None, pcr_exam_date=None):
        self.__cpf = cpf
        self.__name = name
        self.__birthday = birthday
        self.__address = Address(cep, street, number, complement)
        self.__pcr_exam = PCRExam(has_covid, pcr_exam_date)
        self.__has_two_vaccines = has_two_vaccines

    def to_raw(self, address_str=True):
        has_pcr_exam = self.pcr_exam.has_covid != None and self.pcr_exam.date != None
        print('has_pcr_exam', has_pcr_exam)

        obj = {
            "name": self.name,
            "cpf": self.cpf,
            "birthday": self.birthday.strftime('%d/%m/%Y'),
            "address": self.address.to_raw_str() if address_str else self.address.to_raw(),
            "has_two_vaccines": self.has_two_vaccines,
            "has_pcr_exam": has_pcr_exam,
            'pcr_exam': self.pcr_exam.to_raw()
        }

        return obj

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
    def birthday(self, birthday):
        self.__birthday = birthday

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address: Address):
        self.__address = address

    @property
    def pcr_exam(self):
        return self.__pcr_exam

    @pcr_exam.setter
    def pcr_exam(self, pcr_exam: PCRExam):
        self.__pcr_exam = pcr_exam

    @property
    def has_two_vaccines(self):
        return self.__has_two_vaccines

    @has_two_vaccines.setter
    def has_two_vaccines(self, has_two_vaccines: str):
        self.__has_two_vaccines = has_two_vaccines
