from datetime import datetime
from core.exceptions.user_exit_exception import UserExitException
from core.constants import DEFAULT_TITLE
from core.utils.date_validator import validate_datetime, validate_time
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

            if (values['title'].strip() == ''):
                self.show_error_message('Título não pode ser vazio')
                continue

            if (values['max_participants'].strip() == ''):
                self.show_error_message('Max Participantes não pode ser vazio')
                continue

            if (not values['max_participants'].isnumeric()):
                self.show_error_message('Max Participantes deve ser um número')
                continue

            if (int(values['max_participants']) <= 0):
                self.show_error_message(
                    'O número máximo de participantes deve ser maior que 0')
                continue

            if (values['datetime'].strip() == ''):
                self.show_error_message('Data não pode ser vazio')
                continue

            is_date_valid = validate_datetime(values['datetime'])
            if (not is_date_valid):
                self.show_error_message(
                    'Formato de data invalido')
                continue

            date_time_split = values['datetime'].split(' ')
            date_split = date_time_split[0].split('/')
            hour_split = date_time_split[1].split(':')
            datetime_final = datetime(
                int(date_split[2]),
                int(date_split[1]),
                int(date_split[0]),
                int(hour_split[0]),
                int(hour_split[1])
            )
            values['datetime'] = datetime_final

            values['max_participants'] = int(values['max_participants'])

            return values

    def __mount_register_event_window(self, event_data=None):
        defaults = {}

        if (event_data != None):
            defaults = {
                "title": event_data['title'],
                "max_participants": str(event_data['max_participants']),
                "datetime": event_data['datetime'],
            }
        else:
            defaults = {
                "title": '',
                "max_participants": '',
                "datetime": '',
            }

        layout = [
            [sg.Text('Cadastrar Evento')],
            [sg.Text('', key="error_message")],
            [sg.Text('Titulo:')],
            [sg.Input(defaults['title'], key="title",
                      disabled=event_data != None)],
            [sg.Text('Max Participantes:')],
            [sg.Input(defaults['max_participants'], key="max_participants")],
            [sg.Text('Data e Hora (dia/mes/ano hora:min):')],
            [sg.Input(defaults['datetime'], key="datetime")],
            [sg.Submit('Cadastrar'), sg.Button('Cancelar', key='exit')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_events_list(self, events):
        self.__mount_events_list_window(events)
        self.window.read()

    def __mount_events_list_window(self, events):
        values = []
        headings = ['Nome', 'Participantes', 'Data', 'Local', 'Organizadores']
        for event in events:
            values.append([
                event['title'],
                str(len(event['participants'])) +
                '/' + str(event['max_participants']),
                event['datetime'],
                event['local']['name'],
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
            [sg.Text('Título: ' + event['title'])],
            [sg.Text('Participantes: ' +
                     str(len(event['participants'])) + '/' + str(event['max_participants']))],
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
            [sg.Button('Registrar entrada',
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
            self.close()

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
            [sg.Text('Título:')],
            [sg.Input(key='title')],
            [sg.Submit('Procurar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_participants_list(self, title, participants_assoc, hide_covid_proof=False):
        self.__mount_participants_list(
            title, participants_assoc, hide_covid_proof)
        self.window.read()

    def __mount_participants_list(self, title, participants_assoc, hide_covid_proof=False):
        values = []
        headings = ['Nome', 'CPF', 'Aniversario',
                    'Endereco', 'Entrada']

        def create_participant_entrance_str():
            res_str = ''

            res_str += (participant_assoc['time_entrance']
                        if participant_assoc['time_entrance'] else 'x')
            res_str += ' -> '
            res_str += (participant_assoc['time_leave']
                        if participant_assoc['time_leave'] else 'x')

            return res_str

        if (not hide_covid_proof):
            headings.append('Comprovação Covid')

        for participant_assoc in participants_assoc:
            arr = [
                participant_assoc['participant']['name'],
                participant_assoc['participant']['cpf'],
                participant_assoc['participant']['birthday'],
                participant_assoc['participant']['address'],
                create_participant_entrance_str()
            ]

            if (not hide_covid_proof):
                arr.append(
                    'Sim' if participant_assoc['participant']['has_covid_proof'] else 'Não')

            values.append(arr)

        layout = [
            [sg.Text(title)],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_get_hour(self, title):
        self.__mount_show_get_hour(title)

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                self.close()
                raise UserExitException()

            is_time_valid = validate_time(values['hour'])
            if (not is_time_valid):
                self.show_error_message('Formato de horário inválido')
                continue

            hour_raw_split = values['hour'].split(':')
            hour = int(hour_raw_split[0])
            minute = int(hour_raw_split[1])

            return hour, minute

    def __mount_show_get_hour(self, title):
        layout = [
            [sg.Text(title)],
            [sg.Text('', key='error_message')],
            [sg.Text('Horário (hora:min):')],
            [sg.Input(key='hour')],
            [sg.Submit('Confirmar'), sg.Button('Cancelar', key='exit')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)
