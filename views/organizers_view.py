from datetime import datetime
from core.exceptions.user_exit_exception import UserExitException
from core.utils.date_validator import validate_date
from views.ui_view import UIView
from core.constants import DEFAULT_TITLE
import PySimpleGUI as sg


class OrganizersView(UIView):
    def __init__(self):
        super().__init__()

    def show_organizers_menu(self):
        self.__mount_menu_window()
        button, _ = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Organizadores')],
            [sg.Button('Cadastrar organizador',
                       key='register_organizer', size=(30, None))],
            [sg.Button('Editar organizador',
                       key='edit_organizer', size=(30, None))],
            [sg.Button('Remover organizador',
                       key='remove_organizer', size=(30, None))],
            [sg.Button('Listar organizadores',
                       key='list_organizers', size=(30, None))],
            [sg.Button('Procurar organizador',
                       key='find_organizer', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_organizer_register(self, organizer_data=None, remount=True):
        if (remount):
            self.__mount_register_organizer_window(organizer_data)

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['name'] == ''):
                self.show_error_message('Nome não pode ser vazio')
                continue

            if (values['cpf'] == ''):
                self.show_error_message('CPF não pode ser vazio')
                continue

            if (len(values['cpf']) != 11):
                self.show_error_message('CPF deve ter 11 caracteres')
                continue

            if (values['birthday'] == ''):
                self.show_error_message('Data Nascimento não pode ser vazio')
                continue

            is_birthday_valid = validate_date(values['birthday'])
            if (not is_birthday_valid):
                self.show_error_message(
                    'Formato de data em aniversario invalido')
                continue

            birthday_raw_split = values['birthday'].split("/")
            values['birthday'] = datetime(
                int(birthday_raw_split[2]),
                int(birthday_raw_split[1]),
                int(birthday_raw_split[0])
            )

            current = datetime.now()
            if (current.year - values['birthday'].year > 150):
                self.show_error_message(
                    'O usuário não pode ter mais que 150 anos!')
                continue

            return values

    def __mount_register_organizer_window(self, user_data=None):
        defaults = {}

        if (user_data != None):
            defaults = {
                "name": user_data['name'],
                "cpf": user_data['cpf'],
                "birthday": user_data['birthday'],
            }
        else:
            defaults = {
                "name": '',
                "cpf": '',
                "birthday": '',
            }

        layout = [
            [sg.Text('Editar pessoa' if user_data else 'Registrar pessoa')],
            [sg.Text('', key="error_message")],
            [sg.Text('Nome:')],
            [sg.Input(defaults['name'], key='name')],
            [sg.Text('CPF:')],
            [sg.Input(defaults['cpf'], key='cpf', disabled=user_data != None)],
            [sg.Text('Data Nascimento (dia/mes/ano):')],
            [sg.Input(defaults['birthday'], key='birthday')],
            [sg.Submit('Registar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout, finalize=True)

    def show_find_organizer(self):
        self.__mount_find_organizer_window()

        while (True):
            button, values = self.window.read()
            self.close()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['cpf'].strip() == ''):
                self.show_error_message('CPF não deve ser vazio')
                continue

            return values

    def __mount_find_organizer_window(self):
        layout = [
            [sg.Text('Encontrar organizador')],
            [sg.Text('', key='error_message')],
            [sg.Text('CPF')],
            [sg.Input(key='cpf')],
            [sg.Submit('Procurar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_find_many_organizers(self, selected_organizers):
        self.__mount_find_many_organizers_window(selected_organizers)

        while (True):
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                self.close()
                raise(UserExitException)

            if (button == 'confirm' and len(selected_organizers) == 0):
                self.show_error_message(
                    'Você deve selecionar ao menos um organizador')
                continue

            if (button != 'confirm' and values['cpf'].strip() == ''):
                self.show_error_message('CPF não deve ser vazio')
                continue

            return button, values

    def __mount_find_many_organizers_window(self, selected_organizers):
        def create_selected_organizers_str():
            text = ''
            for index, organizer in enumerate(selected_organizers):
                text += organizer['name'] + ' (' + organizer['cpf'] + ')'
                if (index != len(selected_organizers) - 1):
                    text += ', '
            return text

        layout = [
            [sg.Text('Encontrar organizador')],
            [sg.Text('', key='error_message')],
            [sg.Text('Selecionados:')],
            [sg.Text(create_selected_organizers_str())],
            [sg.Text('CPF:')],
            [sg.Input(key='cpf')],
            [sg.Submit('Procurar'), sg.Button(
                'Confirmar esses organizadores', key='confirm'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_organizers_list(self, organizers):
        self.__mount_organizers_list_window(organizers)
        self.window.read()

    def __mount_organizers_list_window(self, organizers):
        values = []
        headings = ['Nome', 'CPF', 'Aniversario',
                    'Endereco']
        for user in organizers:
            values.append([
                user['name'],
                user['cpf'],
                user['birthday'],
                user['address']
            ])

        layout = [
            [sg.Text('Lista de Organizadores')],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_organizer_details(self, organizer):
        self.__mount_organizer_details_window(organizer)
        self.window.read()
        self.window.close()

    def __mount_organizer_details_window(self, user):
        layout = [
            [sg.Text('Detalhes Pessoa')],
            [sg.Text('Nome: ' + user['name'])],
            [sg.Text('CPF: ' + user['cpf'])],
            [sg.Text('Endereço: ' + user['address'])],
            [sg.Text('Aniversario: ' + user['birthday'])],
            [sg.Submit('Voltar')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)
