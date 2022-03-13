
import PySimpleGUI as sg
from core.constants import DEFAULT_TITLE
from core.exceptions.user_exit_exception import UserExitException
from views.ui_view import UIView


class LocalsView(UIView):
    def __init__(self):
        super().__init__()
        print(self.window)

    def show_locals_menu(self):
        self.__mount_menu_window()
        button, _ = self.window.read()
        print('show_locals_menu', button, _, self.window)
        self.close()

        if (button is None or button == 'exit'):
            raise(UserExitException)

        return button

    def __mount_menu_window(self):
        self.close()
        layout = [
            [sg.Text('Menu Locais')],
            [sg.Button('Cadastrar local', key='register_local', size=(30, None))],
            [sg.Button('Editar local', key='edit_local', size=(30, None))],
            [sg.Button('Remover local', key='remove_local', size=(30, None))],
            [sg.Button('Listar locais', key='list_locals', size=(30, None))],
            [sg.Button('Procurar local', key='find_local', size=(30, None))],
            [sg.Button('Sair', key='exit', size=(30, None))],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_register_local(self):
        self.__mount_register_local_window()

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['name'].strip() == ''):
                self.show_error_message('Nome não pode ser vazio')
                continue

            return values

    def __mount_register_local_window(self):
        layout = [
            [sg.Text('Cadastrar local')],
            [sg.Text('', key='error_message')],
            [sg.Text('Nome')],
            [sg.Input(key='name')],
            [sg.Submit('Cadastrar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def __mount_find_local_window(self):
        layout = [
            [sg.Text('Encontrar local')],
            [sg.Text('', key='error_message')],
            [sg.Text('Nome')],
            [sg.Input(key='name')],
            [sg.Submit('Procurar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_find_local(self):
        self.__mount_find_local_window()
        while (True):
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                raise(UserExitException)

            if (values['name'].strip() == ''):
                self.show_error_message('Nome não deve ser vazio')
                continue

            return values

    def show_locals_list(self, locals):
        self.__mount_locals_list_window(locals)
        self.window.read()
        self.close()

    def __mount_locals_list_window(self, locals):
        values = []
        headings = ['Nome', 'Endereco']

        for local in locals:
            values.append([
                local['name'],
                local['address']
            ])

        layout = [
            [sg.Text('Lista Locais')],
            [sg.Table(values=values, headings=headings)],
            [sg.Submit('Voltar')]
        ]

        self.window = sg.Window(DEFAULT_TITLE, layout)

    def show_local(self, local):
        self.__mount_locals_details_window(local)
        self.window.read()
        self.close()

    def __mount_locals_details_window(self, local):
        layout = [
            [sg.Text('Detalhes Local')],
            [sg.Text('Nome: ' + local['name'])],
            [sg.Text('Endereço: ' + local['address'])],
            [sg.Submit('Voltar')]
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)
