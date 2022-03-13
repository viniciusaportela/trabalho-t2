from datetime import datetime
from core.persistance.store import Store
from models.local_model import Local


class LocalStore(Store):
    def __init__(self):
        super().__init__('locals', self.__inject_data)

    def __inject_data(self):
        local = Local(
            'Shopping Trindade', '8800000', 'rua Almeida', '30', 'Loja 2')

        self.add(local)

        super().save()

    def add(self, local: Local):
        super().add(local.name, local)
        super().save()

    def remove(self, name):
        super().remove(name)
        super().save()

    def update(self, local: Local):
        super().update(local.name, local)
        super().save()

    def list(self):
        return super().list()

    def get(self, name):
        return super().get(name)
