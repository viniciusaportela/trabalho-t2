from datetime import date, datetime
from core.exceptions.user_exit_exception import UserExitException
from core.constants import DEFAULT_TITLE
from core.utils.date_validator import validate_date, validate_datetime, validate_time
from core.utils.recurring_ask import recurring_ask
from views.ui_view import UIView
import PySimpleGUI as sg


class EventsView(UIView):
    def __init__(self):
        super().__init__()

    def show_events_menu(self):
        self.__mount_menu_window()
        button, _ = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Eventos')],
            [sg.Button('Cadastrar evento', key='register_event', size=(30, None))],
            [sg.Button('Editar evento', key='edit_event', size=(30, None))],
            [sg.Button('Remover evento', key='remove_event', size=(30, None))],
            [sg.Button('Listar eventos', key='list_events', size=(30, None))],
            [sg.Button('Procurar evento', key='find_event', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_register_event(self, event_data=None):
        self.__mount_register_event_window(event_data)

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            is_date_valid = validate_date(values['date'])
            if (not is_date_valid):
                self.show_error_message(
                    'Formato de data invalido')
                continue

            date_time_split = values['date'].split(' ')
            date_split = date_time_split[0].split('/')
            hour_split = date_time_split[1].split(':')
            datetime_final = date(
                int(date_split[2]),
                int(date_split[1]),
                int(date_split[0]),
                int(hour_split[0]),
                int(hour_split[1])
            )
            values['date'] = datetime_final

            if (not values['max_participants'].isnumeric()):
                self.show_error_message('Max Participantes deve ser numérico')
                continue

            return values

    def __mount_register_event_window(self, event_data=None):
        defaults = {}

        if (event_data != None):
            defaults = {
                "title": event_data['title'],
                "max_participants": event_data['max_participants'],
                "date": event_data['date'],
            }
        else:
            defaults = {
                "title": '',
                "max_participants": '',
                "date": '',
            }

        layout = [
            [sg.Text('Cadastrar Evento')],
            [sg.Text('', key="error_message")],
            [sg.Text('Título:')]
            [sg.Input(defaults['title'], key="title",
                      disabled=event_data != None)],
            [sg.Text('Max Participantes:')],
            [sg.Input(defaults['max_participants'], key="max_participants")],
            [sg.Text('Data e Hora (dia/mes/ano hora:min):')],
            [sg.Input(defaults['date'], key="date")],
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_events_list(self, events):
        self.__mount_events_list_window(events)
        self.window.read()

    def __mount_events_list_window(self, events):
        values = []
        headings = ['Nome', 'Data', 'Endereco', 'Local', 'Organizadores']
        for event in events:
            values.append([
                event['name'],
                event['datetime'],
                event['address'],
                event['local'],
                event['organizers']
            ])

        layout = [
            [sg.Text('Lista de Eventos')],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_event_menu(self, event):
        self.__mount_event_menu_window(event)
        button, _ = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_event_menu_window(self, event):
        layout = [
            [sg.Text('Evento')],
            [sg.Text('Título: ' + event['name'])],
            [sg.Text('Participantes: ' +
                     len(event['participants'] + '/' + str(event.max_participants)))],
            [sg.Text('Data: ' + event['datetime'])],
            [sg.Text('Local: ' + event['local']['name'])],
            [sg.Text('Organizadores: ' + event['organizers'])],
            [sg.Text('')],
            [sg.Button('Adicionar participante',
                       key='add_participant', size=(30, None))],
            [sg.Button('Listar participantes',
                       key='list_participants', size=(30, None))],
            [sg.Button('Listar participantes com comprovação Covid',
                       key='list_participants_with_covid_proof', size=(30, None))],
            [sg.Button('Listar participantes sem comprovação Covid',
                       key='list_participants_without_covid_proof', size=(30, None))],
            [sg.Button('Listar entrada',
                       key='register_entrance', size=(30, None))],
            [sg.Button('Registrar saída',
                       key='register_leave', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_find_event(self):
        self.__mount_find_event_window()

        while (True):
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['title'].strip() == ''):
                self.show_error_message('Título não deve ser vazio')
                continue

            return values

    def __mount_find_event_window(self):
        layout = [
            [sg.Text('Encontrar evento')],
            [sg.Text('', key='error_message')],
            [sg.Text('Title')],
            [sg.Input(key='title')],
            [sg.Submit('Procurar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_participants_list(self, participants_assoc):
        self.__mount_participants_list(participants_assoc)
        self.window.read()

    def __mount_participants_list(self, participant_assoc):
        values = []
        headings = ['Nome', 'CPF', 'Aniversario',
                    'Endereco', 'Tem comprovação Covid']
        for participant in participant_assoc:
            values.append([
                participant['name'],
                participant['cpf'],
                participant['birthday'],
                participant['address'],
                'Sim' if participant['has_covid_proof'] else 'Não'
            ])

        layout = [
            [sg.Text('Lista de Pessoas')],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_get_hour(self):
        self.__mount_show_get_hour()

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise UserExitException()

            is_time_valid = validate_time(values['hour'])
            if (not is_time_valid):
                self.show_error_message('Formato de horário inválido')
                continue

            hour_raw_split = values['hour'].split(':')
            hour = int(hour_raw_split[0])
            minute = int(hour_raw_split[1])

            return hour, minute

    def __mount_show_get_hour(self):
        layout = [
            [sg.Text('Horário')],
            [sg.Input(key='hour')],
            [sg.Submit('Confirmar'), sg.Button('Cancelar', key='exit')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)
