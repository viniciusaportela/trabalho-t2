from datetime import datetime
from core.persistance.store import Store
from models.organizer_model import Organizer


class OrganizerStore(Store):
    def __init__(self):
        print('organizer_store init')
        super().__init__('organizers', self.__inject_data)

    def __inject_data(self):
        organizer1 = Organizer('12312312399', 'Jose', datetime(
            2000, 2, 5), '8800000', 'rua Almeida', '10', '')

        self.add(organizer1)

        super().save()

    def add(self, organizer: Organizer):
        super().add(organizer.cpf, organizer)
        super().save()

    def remove(self, cpf):
        super().remove(cpf)
        super().save()

    def update(self, organizer: Organizer):
        super().update(organizer.cpf, organizer)
        super().save()

    def list(self):
        return super().list()

    def get(self, cpf):
        return super().get(cpf)
