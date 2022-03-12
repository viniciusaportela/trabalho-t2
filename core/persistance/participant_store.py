from datetime import datetime
from core.persistance.store import Store
from models.participant_model import Participant


class ParticipantStore(Store):
    def __init__(self):
        super().__init__('participants')
        if (not self.exists):
            self.__inject_data()

    def __inject_data(self):
        self.add('12312312314', 'Vinicius', datetime(2001, 7, 4),
                 '8800000', 'rua porto', '220', 'apt 100')
        self.add('12312312313', 'Jose', datetime(2000, 2, 5),
                 '8800000', 'rua Almeida', '10', '', True)

    def add(participant: Participant):
        super().add(participant)

    def remove(cpf):
        super().remove(cpf)

    def update(cpf, participant: Participant):
        pass

    def list():
        super().list()

    def get(cpf):
        super().get(cpf)
