from core.exceptions.user_exit_exception import UserExitException
from core.constants import DEFAULT_TITLE
from views.ui_view import UIView
import PySimpleGUI as sg


class ReportsView(UIView):
    def show_reports_menu(self):
        self.__mount_menu_window()
        button, _ = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Relatórios')],
            [sg.Button('Eventos a realizar',
                       key='soon_events', size=(30, None))],
            [sg.Button('Ranking de eventos por número de participantes',
                       key='ranking_events', size=(30, None))],
            [sg.Button('Eventos já realizados',
                       key='past_events', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_report_events(self, title, events):
        self.__mount_reports_events(title, events)
        self.window.read()
        self.close()

    def __mount_reports_events(self, title, events):
        values = []
        headings = ['Título', 'Local', 'Data',
                    'Participantes']

        for event in events:
            values.append([
                event['title'],
                event['local']['name'],
                event['datetime'],
                len(event['participants']),
            ])

        layout = [
            [sg.Text(title)],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)
