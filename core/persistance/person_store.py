from core.persistance.store import Store


class PersonStore(Store):
    def __init__(self):
        super().__init__('people')