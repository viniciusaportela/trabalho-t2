from datetime import datetime
from views.reports_view import ReportsView


class ReportsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.view = ReportsView()
    
    def open_reports_menu(self):
        bindings = {
            1: self.open_soon_events,
            2: self.open_events_ranking_by_participants,
            3: self.open_past_events
        }

        while True:
            option = self.view.show_reports_menu()

            if (option == 0):
                return

            bindings[option]()
    
    def open_soon_events(self):
        events = self.__controllers_manager.event.get_events()

        soon_events = []
        for event in events:
            current = datetime.now()
            if (event.datetime > current):
                # TODO dict
                soon_events.append(event)
        
        soon_events_sorted = self.__sort_events_by_date(soon_events, False)

        self.view.show_report_events(soon_events_sorted, '-----------= Proximos Eventos =-----------')

    def open_events_ranking_by_participants(self):
        events = self.__controllers_manager.event.get_events()

        events_sorted = self.__sort_events_by_participants_count(events)    

        self.view.show_report_events(events_sorted, '-----------= Ranking por participantes =-----------', True)

    def open_past_events(self):
        events = self.__controllers_manager.event.get_events()
        
        past_events = []
        for event in events:
            current = datetime.now()
            if (event.datetime <= current):
                past_events.append(event)

        past_events_sorted = self.__sort_events_by_date(past_events)

        self.view.show_report_events(past_events_sorted, '-----------= Ultimos Eventos =-----------')

    def __sort_events_by_participants_count(self, events):
        def sort_func(event):
            return len(event.participants)

        return sorted(events, key=sort_func, reverse=True)
    
    def __sort_events_by_date(self, events, reverse = True):
        def sort_func(event):
            return event.datetime

        return sorted(events, key=sort_func, reverse=reverse)