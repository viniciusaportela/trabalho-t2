from utils.recurring_ask import recurring_ask


class AddressView:
    def show_register_address(self):
        def ask_address_cep():
            cep = input('CEP: ')
            if (not cep.isnumeric()):
                return None
            return cep
        cep = recurring_ask(ask_address_cep)
        
        street = input('Rua: ')
        
        def ask_address_number():
            number = input('Numero: ')
            if (not number.isnumeric()):
                return None
            return number
        number = recurring_ask(ask_address_number)
        
        complement = input('Complemento: ')

        return { 
            "cep": cep, 
            "street": street, 
            "number": number, 
            "complement": complement
        }