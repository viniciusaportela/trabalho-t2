from datetime import datetime
from core.exceptions.user_exit_exception import UserExitException
from views.reports_view import ReportsView


class ReportsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.view = ReportsView()

    def open_reports_menu(self):
        try:
            bindings = {
                'soon_events': self.open_soon_events,
                'ranking_events': self.open_events_ranking_by_participants,
                'past_events': self.open_past_events,
            }

            while True:
                option = self.view.show_users_menu()
                bindings[option]()
        except UserExitException:
            return

    def open_soon_events(self):
        events = self.__controllers_manager.event.get_events()

        soon_events = []
        for event in events:
            current = datetime.now()
            if (event.datetime > current):
                soon_events.append(event)

        soon_events_sorted = self.__sort_events_by_date(soon_events, False)
        for index, event in enumerate(soon_events_sorted):
            soon_events_sorted[index] = event.to_raw()

        self.view.show_report_events('Próximos Eventos', soon_events_sorted)

    def open_events_ranking_by_participants(self):
        events = self.__controllers_manager.event.get_events()

        events_sorted = self.__sort_events_by_participants_count(events)
        for index, event in enumerate(events_sorted):
            events_sorted[index] = event.to_raw()

        self.view.show_report_events(
            'Ranking por participantes', events_sorted)

    def open_past_events(self):
        events = self.__controllers_manager.event.get_events()

        past_events = []
        for event in events:
            current = datetime.now()
            if (event.datetime <= current):
                past_events.append(event)

        past_events_sorted = self.__sort_events_by_date(past_events)

        for index, event in enumerate(past_events_sorted):
            past_events_sorted[index] = event.to_raw()

        self.view.show_report_events('Últimos Eventos', past_events_sorted)

    def __sort_events_by_participants_count(self, events):
        def sort_func(event):
            return len(event.participants)

        return sorted(events, key=sort_func, reverse=True)

    def __sort_events_by_date(self, events, reverse=True):
        def sort_func(event):
            return event.datetime

        return sorted(events, key=sort_func, reverse=reverse)
