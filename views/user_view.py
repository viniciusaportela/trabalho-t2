from datetime import datetime
import json
from core.constants import DEFAULT_TITLE
from core.errors.user_exit_exception import UserExitException
from core.utils.date_validator import validate_date
from core.utils.recurring_ask import recurring_ask
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

    def show_user_register(self, user_data=None):
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

            if (
                not values['has_pcr_exam'] or
                values['pcr_exam_result'] == '--' or
                values['pcr_exam_date'].strip() == ''
            ):
                values['pcr_exam_result'] = None
                values['has_pcr_exam'] = False
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
                defaults['pcr_exam_result'] = user_data['pcr_exam']['has_covid'] if user_data['pcr_exam']['has_covid'] != None else '--',
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
            [sg.Submit('Registar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout, finalize=True)

    def __mount_find_user_window(self):
        layout = [
            [sg.Text('Encontrar pessoa')],
            [sg.Text('', key='error_message')],
            [sg.Text('CPF')],
            [sg.Input(key='cpf')],
            [sg.Submit('Procurar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_find_user(self):
        self.__mount_find_user_window()

        while (True):
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['cpf'].strip() == ''):
                self.show_error_message('CPF não deve ser vazio')
                continue

            return values

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

    def show_user_list(self, users):
        self.__mount_user_list_window(users)
        self.window.read()

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
            [sg.Text('Aniversario: ' + user['birthday'])],
            [sg.Text('Tomou 2 doses: ' +
                     ('Sim' if user['has_two_vaccines'] else 'Não'))],
            [sg.Text('Exame PCR: ' + get_pcr_exam_text())],
            [sg.Submit('Voltar')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_participant_register(self, skip_first_ask=False):
        has_covid_proof = True
        if (not skip_first_ask):
            def ask_has_covid_proof():
                has_covid_proof = input(
                    "Tem alguma comprovacao contra covid (s/n)? ").lower()
                if (has_covid_proof != 's' and has_covid_proof != 'n'):
                    return None
                return has_covid_proof == 's'
            has_covid_proof = recurring_ask(ask_has_covid_proof)

        if not has_covid_proof:
            return {"has_two_vaccines": None, "has_covid": None, "pcr_exam_date": None}

        def ask_has_covid_proof():
            has_two_vaccines = input('Tomou duas doses (s/n)? ').lower()
            if (has_two_vaccines != 's' and has_two_vaccines != 'n'):
                return None
            return has_two_vaccines == 's'
        has_two_vaccines = recurring_ask(ask_has_covid_proof)

        if (has_two_vaccines):
            return {"has_two_vaccines": has_two_vaccines, "has_covid": None, "pcr_exam_date": None}

        has_pcr_test = input('Fez um teste PCR (s/n)? ') == 's'

        if (not has_pcr_test):
            return {"has_two_vaccines": None, "has_covid": None, "pcr_exam_date": None}

        def ask_pcr_exam_has_covid():
            has_covid = input('Qual resultado do exame(positivo/negativo)? ')
            if (has_covid != 'positivo' and has_covid != 'negativo'):
                return None
            return has_covid == 'positivo'
        has_covid = recurring_ask(ask_pcr_exam_has_covid)

        def ask_pcr_exam_date():
            pcr_exam_date_raw = input(
                'Qual foi a data do exame (dia/mes/ano)? ')
            date_is_valid = validate_date(pcr_exam_date_raw)
            if (not date_is_valid):
                return None

            pcr_exam_date_raw_splitted = pcr_exam_date_raw.split("/")
            pcr_exam_date = datetime(
                int(pcr_exam_date_raw_splitted[2]),
                int(pcr_exam_date_raw_splitted[1]),
                int(pcr_exam_date_raw_splitted[0])
            )
            return pcr_exam_date
        pcr_exam_date = recurring_ask(ask_pcr_exam_date)

        return {"has_two_vaccines": False, "has_covid": has_covid, "pcr_exam_date": pcr_exam_date}
