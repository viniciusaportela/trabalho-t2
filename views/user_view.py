from datetime import datetime
from core.constants import DEFAULT_TITLE
from core.exceptions.user_exit_exception import UserExitException
from core.utils.date_validator import validate_date
import PySimpleGUI as sg
from views.ui_view import UIView


class UserView(UIView):
    def __init__(self):
        super().__init__()

    def show_users_menu(self):
        self.__mount_menu_window()
        button, _ = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Pessoas')],
            [sg.Button('Cadastrar Pessoa', key='register_user', size=(30, None))],
            [sg.Button('Editar pessoa', key='edit_user', size=(30, None))],
            [sg.Button('Remover pessoa', key='remove_user', size=(30, None))],
            [sg.Button('Listar Pessoas', key='list_users', size=(30, None))],
            [sg.Button('Procurar Pessoa', key='find_user', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_user_register(self, user_data=None, remount=True):
        if (remount):
            self.__mount_user_register_window(user_data)

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
                    'Formato de data em aniversario inválido')
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

            if (values['has_pcr_exam']):
                date_is_valid = validate_date(values['pcr_exam_date'])
                if (not date_is_valid):
                    self.show_error_message(
                        'Formato de data do exame inválido')
                    continue

                pcr_exam_date_raw_splitted = values['pcr_exam_date'].split("/")
                pcr_exam_date = datetime(
                    int(pcr_exam_date_raw_splitted[2]),
                    int(pcr_exam_date_raw_splitted[1]),
                    int(pcr_exam_date_raw_splitted[0])
                )
                values['pcr_exam_date'] = pcr_exam_date

                if (values['pcr_exam_result'] != 'positivo' and values['pcr_exam_result'] != 'negativo'):
                    self.show_error_message(
                        'O resultado do exame deve ser positivo ou negativo')
                    continue
            else:
                values['pcr_exam_result'] = None
                values['pcr_exam_date'] = None

            return values

    def __mount_user_register_window(self, user_data=None):
        defaults = {}

        if (user_data != None):
            defaults = {
                "name": user_data['name'],
                "cpf": user_data['cpf'],
                "birthday": user_data['birthday'],
                "has_two_vaccines": user_data['has_two_vaccines'],
                "has_pcr_exam": user_data['has_pcr_exam'],
                "pcr_exam_result": "--",
                "pcr_exam_date": '',
            }

            if (user_data['has_pcr_exam']):
                defaults['pcr_exam_result'] = ('positivo' if user_data['pcr_exam']['has_covid']
                                               else 'negativo') if user_data['pcr_exam']['has_covid'] != None else '--',
                defaults['pcr_exam_date'] = user_data['pcr_exam']['pcr_exam_date']
        else:
            defaults = {
                "name": '',
                "cpf": '',
                "birthday": '',
                "has_two_vaccines": False,
                "has_pcr_exam": False,
                "pcr_exam_result": "--",
                "pcr_exam_date": '',
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
            [sg.HorizontalSeparator()],
            [sg.Checkbox('Tomou 2 doses', key='has_two_vaccines',
                         default=defaults['has_two_vaccines'])],
            [sg.Checkbox('Fez exame PCR', key='has_pcr_exam',
                         default=defaults['has_pcr_exam'])],
            [sg.Text('Resultado exame PCR (se fez):')],
            [sg.Combo(['--', 'positivo', 'negativo'],
                      default_value=defaults['pcr_exam_result'], key='pcr_exam_result')],
            [sg.Text('Data exame PCR (dia/mes/ano) (se fez):')],
            [sg.Input(defaults['pcr_exam_date'], key='pcr_exam_date')],
            [sg.Submit('Cadastrar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout, finalize=True)

    def show_find_user(self, users_dict, title='Encontrar pessoa'):
        self.__mount_find_user_window(title, users_dict)

        button, values = self.window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return values

    def __mount_find_user_window(self, title, users):
        def mount_list():
            arr = []
            for user in users:
                arr.append(user['name'] + ' (' + user['cpf'] + ')')
            return arr
        values = mount_list()

        layout = [
            [sg.Text(title)],
            [sg.Text('Usuário')],
            [sg.Combo(values, default_value=values[0], key='user')],
            [sg.Submit('Confirmar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_user_list(self, users):
        self.__mount_user_list_window(users)
        self.window.read()

    def __mount_user_list_window(self, users):
        values = []
        headings = ['Nome', 'CPF', 'Aniversario',
                    'Endereco', 'Tomou 2 doses']
        for user in users:
            values.append([
                user['name'],
                user['cpf'],
                user['birthday'],
                user['address'],
                'Sim' if user['has_two_vaccines'] else 'Não'
            ])

        layout = [
            [sg.Text('Lista de Pessoas')],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_user_details(self, user):
        self.__mount_user_details_window(user)
        self.window.read()
        self.window.close()

    def __mount_user_details_window(self, user):
        def get_pcr_exam_text():
            if ('pcr_exam' in user):
                return 'Positivo' if user['pcr_exam']['has_covid'] else 'Negativo'

            return 'Não realizado'

        layout = [
            [sg.Text('Detalhes Pessoa')],
            [sg.Text('Nome: ' + user['name'])],
            [sg.Text('CPF: ' + user['cpf'])],
            [sg.Text('Endereço: ' + user['address'])],
            [sg.Text('Aniversario: ' + user['birthday'])],
            [sg.Text('Tomou 2 doses: ' +
                     ('Sim' if user['has_two_vaccines'] else 'Não'))],
            [sg.Text('Exame PCR: ' + get_pcr_exam_text())],
            [sg.Submit('Voltar')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)
