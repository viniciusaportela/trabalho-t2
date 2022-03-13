from models.address_model import Address
from models.person_model import Person
from models.pcr_exam_model import PCRExam


class Participant(Person):
    def __init__(self, cpf, name, birthday, cep, street, number, complement, has_two_vaccines=None, has_covid=None, pcr_exam_date=None):
        super().__init__(cpf, name, birthday, cep, street, number, complement)
        self.__pcr_exam = PCRExam(has_covid, pcr_exam_date)
        self.__has_two_vaccines = has_two_vaccines

    def to_raw(self, address_str=True):
        has_pcr_exam = self.pcr_exam.has_covid != None and self.pcr_exam.date != None

        return {
            "name": self.name,
            "cpf": self.cpf,
            "birthday": self.birthday.strftime('%d/%m/%Y'),
            "address": self.address.to_raw_str() if address_str else self.address.to_raw(),
            "has_two_vaccines": self.has_two_vaccines,
            "has_pcr_exam": has_pcr_exam,
            'pcr_exam': self.pcr_exam.to_raw()
        }

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
