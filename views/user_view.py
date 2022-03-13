from datetime import datetime
from core.constants import DEFAULT_TITLE
from core.errors.user_exit_exception import UserExitException
from core.utils.date_validator import validate_date
from core.utils.recurring_ask import recurring_ask
import PySimpleGUI as sg
from PySimpleGUI import ErrorElement


class UserView:
    def __init__(self):
        self.__window = None

    def show_error_message(self, error_message: str) -> None:
        error_message_exists = not isinstance(self.__window.find_element(
            'error_message', silent_on_error=True), ErrorElement)
        if (self.__window and error_message_exists):
            self.__window.find_element(
                'error_message', silent_on_error=True).update(error_message, background_color='#f5254b')

    def show_message(self, message):
        sg.Popup(message, keep_on_top=True)

    def open_users_menu(self):
        print('open users')
        self.__create_menu_window()
        button, _ = self.__window.read()
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __create_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Pessoas')],
            [sg.Button('Cadastrar Pessoa', key='register_user', size=(30, None))],
            [sg.Button('Editar pessoa', key='edit_user', size=(30, None))],
            [sg.Button('Remover pessoa', key='delete_user', size=(30, None))],
            [sg.Button('Listar Pessoas', key='list_users', size=(30, None))],
            [sg.Button('Procurar Pessoa', key='find_user', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.__window = sg.Window(DEFAULT_TITLE, layout)

    def show_user_register(self, user_data=None):
        self.__create_user_register_window(user_data)
        self.__window.find_element('pcr_exam_result').update(value='--')

        while True:
            button, values = self.__window.read()

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

    def __create_user_register_window(self, user_data=None):
        self.close()
        layout = [
            [sg.Text('Editar pessoa' if user_data else 'Registrar pessoa')],
            [sg.Text('', key="error_message")],
            [sg.Text('Nome:')],
            [sg.Input(key='name')],
            [sg.Text('CPF:')],
            [sg.Input(key='cpf')],
            [sg.Text('Data Nascimento (dia/mes/ano):')],
            [sg.Input(key='birthday')],
            [sg.HorizontalSeparator()],
            [sg.Checkbox('Tomou 2 doses', key='has_two_vaccines')],
            [sg.Checkbox('Fez exame PCR', key='has_pcr_test')],
            [sg.Text('Resultado exame PCR (se fez):')],
            [sg.Combo(['--', 'positivo', 'negativo'],
                      key='pcr_exam_result')],
            [sg.Text('Data exame PCR (dia/mes/ano) (se fez):')],
            [sg.Input(key='pcr_exam_date')],
            [sg.Submit('Registar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.__window = sg.Window(DEFAULT_TITLE, layout, finalize=True)

    def show_find_user(self, headless=False):
        if (not headless):
            print('-----------= Procurar Pessoa =-----------')
        user_cpf = input('Digite o CPF ou 0 para sair: ')

        if (user_cpf == '0'):
            return None

        return user_cpf

    def show_user_list(self, users):
        print('-----------= Lista de Usuarios =-----------')
        for index, user in enumerate(users):
            print(str(index + 1) + ' - ' + user.name + ' (' + user.cpf + ')')
        input('Aperte enter para sair... ')

    def show_user_details(self, user):
        print('-----------= Usuario =-----------')
        print('Nome: ' + user.name)
        print('CPF: ' + user.cpf)
        print('Aniversario: ' + user.birthday.strftime("%d/%m/%Y"))
        print('Endereco: ' + user.address.cep + ', ' + user.address.street +
              ', n. ' + user.address.number + ', ' + user.address.complement)

        if (user.has_two_vaccines == None):
            print('Tomou duas doses: nao informado')
        else:
            print('Tomou duas doses: ' +
                  ('sim' if user.has_two_vaccines else 'nao'))

        if (user.pcr_exam.date == None):
            print('Exame PCR: nao realizado')
        else:
            print('Exame PCR: ' +
                  ('positivo' if user.pcr_exam.has_covid else 'negativo'))

        input('Aperte enter para sair... ')

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

    def close(self):
        print('open_users_menu close')
        if (self.__window):
            self.__window.close()
