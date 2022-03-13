from datetime import datetime
from core.persistance.store import Store
from models.participant_model import Participant


class ParticipantStore(Store):
    def __init__(self):
        print('participant_store init')
        super().__init__('participants', self.__inject_data)

    def __inject_data(self):
        user1 = Participant('12312312314', 'Vinicius', datetime(2001, 7, 4),
                            '8800000', 'rua porto', '220', 'apt 100')
        user2 = Participant('12312312313', 'Jose', datetime(2000, 2, 5),
                            '8800000', 'rua Almeida', '10', '', True)

        self.add(user1)
        self.add(user2)

        super().save()

    def add(self, participant: Participant):
        super().add(participant.cpf, participant)
        super().save()

    def remove(self, cpf):
        super().remove(cpf)
        super().save()

    def update(self, participant: Participant):
        super().update(participant.cpf, participant)
        super().save()

    def list(self):
        return super().list()

    def get(self, cpf):
        return super().get(cpf)
