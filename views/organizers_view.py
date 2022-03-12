from datetime import datetime
from utils.date_validator import validate_date


class OrganizersView:
    def show_organizers_menu(self):
        while True:
            print('-----------= Menu Organizadores =-----------')
            print('1 - Cadastrar organizador')
            print('2 - Editar organizador')
            print('3 - Deletar organizador')
            print('4 - Listar organizadores')
            print('5 - Procurar organizador')
            print('0 - Voltar')
            option = int(input('Por favor insira uma opcao: ').strip() or '-1')
            if (option >= 0 and option <= 5):
                return option
            else:
                print('Escolha uma opcao valida!')

    def show_register_organizer(self, edit_mode = False):
        print('-----------= Editar Organizador =-----------' if edit_mode else '-----------= Cadastrar Organizador =-----------')
        name = input('Nome: ')
        cpf = None
        if (not edit_mode):
            cpf = input('CPF: ')

        not_valid = True
        birthday = None
        while not_valid:
            birthday_raw = input('Data Nascimento (dia/mes/ano): ')
            is_valid = validate_date(birthday_raw)

            if (is_valid):
                not_valid = False
                birthday_raw_split = birthday_raw.split("/")
                birthday = datetime(
                    int(birthday_raw_split[2]),
                    int(birthday_raw_split[1]),
                    int(birthday_raw_split[0])
                )
            else:
                print('Formato de data invalido! Por favor siga o padrao (dia/mes/ano):')

        return { "name": name, "cpf": cpf, "birthday": birthday }

    def show_find_organizer(self, headless = False, custom_message = ''):
        if (not headless):
            print('-----------= Procurar Organizador =-----------')
        organizer_cpf = input(custom_message or 'Digite o CPF ou 0 para sair: ')

        if (organizer_cpf == '0'):
            return None

        return organizer_cpf

    def show_organizers_list(self, organizers):
        print('-----------= Lista de Organizadores =-----------')
        for index, organizer in enumerate(organizers):
            print(str(index + 1) + ' - ' + organizer.name + ' (' + organizer.cpf + ')')
        input('Aperte enter para sair... ')

    def show_organizer_details(self, organizer):
        print('-----------= Organizador =-----------')
        print('Nome: ' + organizer.name)
        print('CPF: ' + organizer.cpf)
        print('Aniversario: ' + organizer.birthday.strftime("%d/%m/%Y"))
        print('Endereco: ' + organizer.address.cep + ', ' + organizer.address.street + ', n. ' + organizer.address.number + ', ' + organizer.address.complement)
        
        input('Aperte enter para sair... ')