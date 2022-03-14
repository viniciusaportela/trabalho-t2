import PySimpleGUI as sg
from core.constants import DEFAULT_TITLE

from core.exceptions.user_exit_exception import UserExitException


class MainView:
    def __init__(self) -> None:
        self.__setup_theme()

    def __setup_theme(self):
        sg.theme('DarkGrey5')

    def close(self):
        if (self.__window):
            self.__window.close()

    def __mount_window(self):
        layout = [
            [sg.Text('Menu')],
            [sg.Button('Pessoas', key='people', size=(30, None))],
            [sg.Button('Eventos', key='events', size=(30, None))],
            [sg.Button('Organizadores', key='organizers', size=(30, None))],
            [sg.Button('Locais', key='locals', size=(30, None))],
            [sg.Button('Relatorios', key='reports', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.__window = sg.Window(DEFAULT_TITLE, layout)

    def show_menu(self):
        self.__mount_window()
        button, _ = self.__window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def show_message(self, message):
        sg.Popup(message, keep_on_top=True)
