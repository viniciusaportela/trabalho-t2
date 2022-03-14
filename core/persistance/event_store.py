from datetime import datetime
from core.persistance.local_store import LocalStore
from core.persistance.organizer_store import OrganizerStore
from core.persistance.store import Store
from models.event_model import Event


class EventStore(Store):
    def __init__(self, controllers_manager):
        super().__init__('events', self.create_inject_data(controllers_manager))

    def create_inject_data(self, controllers_manager):
        def __inject_data():
            organizer = controllers_manager.organizer.store.get(
                '12312312399')
            local = controllers_manager.local.store.get(
                'Shopping Trindade')

            event1 = Event(
                'E', 25, [], local, datetime(2020, 1, 1, 17, 30), [organizer])
            event2 = Event('E2', 10, [], local,
                           datetime(2022, 2, 22, 17, 30), [organizer])
            event3 = Event('E3', 10, [], local,
                           datetime(2022, 4, 22, 17, 30), [organizer])

            self.add(event1)
            self.add(event2)
            self.add(event3)

            self.save()

        return __inject_data

    def add(self, event: Event):
        super().add(event.title, event)
        super().save()

    def remove(self, title):
        super().remove(title)
        super().save()

    def update(self, event: Event):
        super().update(event.title, event)
        super().save()

    def list(self):
        return super().list()

    def get(self, title):
        return super().get(title)
