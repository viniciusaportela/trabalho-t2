from core.constants import DEFAULT_TITLE
from core.exceptions.user_exit_exception import UserExitException
import PySimpleGUI as sg
from PySimpleGUI import ErrorElement
from views.ui_view import UIView


class AddressView(UIView):
    def __init__(self):
        super().__init__()

    def show_register_address(self, address_data=None):
        self.__mount_register_address_window(address_data)

        while True:
            button, values = self.window.read()

            if (button is None or button == 'exit'):
                self.close()
                raise(UserExitException)

            if (values['cep'] == ''):
                self.show_error_message('CEP não pode ser vazio')
                continue

            if (not values['cep'].isnumeric()):
                self.show_error_message('CEP deve ser um número')
                continue

            if (values['number'] == ''):
                self.show_error_message('Número não pode ser vazio')
                continue

            if (not values['number'].isnumeric()):
                self.show_error_message('Número deve ser um número')
                continue

            if (values['street'] == ''):
                self.show_error_message('Rua não pode ser vazio')
                continue

            return values

    def __mount_register_address_window(self, address_data=None):
        defaults = {}

        if (address_data != None):
            defaults = {
                'cep': address_data['cep'],
                'number': address_data['number'],
                'street': address_data['street'],
                'complement': address_data['complement']
            }
        else:
            defaults = {
                'cep': '',
                'number': '',
                'street': '',
                'complement': ''
            }

        layout = [
            [sg.Text('Adicionar endereço')],
            [sg.Text('', key="error_message")],
            [sg.Text('CEP:')],
            [sg.Input(defaults['cep'], key='cep')],
            [sg.Text('Numero:')],
            [sg.Input(defaults['number'], key='number')],
            [sg.Text('Rua:')],
            [sg.Input(defaults['street'], key='street')],
            [sg.Text('Complemento:')],
            [sg.Input(defaults['complement'], key='complement')],
            [sg.Submit('Registar'), sg.Button(
                'Cancelar', key='exit')],
        ]
        self.window = sg.Window(DEFAULT_TITLE, layout)
