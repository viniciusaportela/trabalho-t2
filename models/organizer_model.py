from models.person_model import Person


class Organizer(Person):
    def __init__(self, cpf, name, birthday, cep, street, number, complement):
        super().__init__(cpf, name, birthday, cep, street, number, complement)

    def to_raw(self, address_str=True):
        return {
            "name": self.name,
            "cpf": self.cpf,
            "birthday": self.birthday.strftime('%d/%m/%Y'),
            "address": self.address.to_raw_str() if address_str else self.address.to_raw(),
        }
