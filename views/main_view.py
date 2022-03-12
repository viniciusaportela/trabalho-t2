import PySimpleGUI as sg

from core.errors.user_interrupt_exception import UserInterrupt

class MainView:
    def __init__(self) -> None:
        self.__init_components()

    def __init_components(self):
        layout = [
            [sg.Text('Menu')], 
            [sg.ReadButton('Pessoas', key='people')],
            [sg.ReadButton('Eventos', key='events')],
            [sg.ReadButton('Organizadores', key='organizers')],
            [sg.ReadButton('Locais', key='locals')],
            [sg.ReadButton('Relatorios', key='reports')],
            [sg.ReadButton('Sair', key='exit')],
        ]
        self.__window = sg.Window('Menu', layout)

    def show_menu(self):
        while True:
            button, _ = self.__window.Read()

            if (button is None or 'exit'):
                raise(UserInterrupt)
            
            self.__window.Close()

            return