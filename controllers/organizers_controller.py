from datetime import datetime
from views.organizers_view import OrganizersView
from models.participant_model import Participant


class OrganizersController:
    def __init__(self, controllers_manager):
        self.__organizers = []
        self.__controllers_manager = controllers_manager
        self.view = OrganizersView()

    def get_organizers(self):
        return self.__organizers

    def get_organizer_by_cpf(self, cpf):
        for index, organizer in enumerate(self.__organizers):
            if organizer.cpf == cpf:
                return organizer, index
        return None, -1

    def add_organizer(self, cpf, name, birthday, cep, street, number, complement):
        already_has_organizer, _ = self.get_organizer_by_cpf(cpf)

        if (already_has_organizer):
            return False, 'Esse organizador ja existe!'

        organizer = Participant(cpf, name, birthday, cep, street, number, complement)
        self.__organizers.append(organizer)

        return True, ''

    def edit_organizer(self, cpf, name, birthday, cep, street, number, complement):
        organizer, index = self.get_organizer_by_cpf(cpf)

        organizer.name = name
        organizer.birthday = birthday
        organizer.cep = cep
        organizer.address.street = street
        organizer.address.number = number
        organizer.address.complement = complement

        self.__organizers[index] = organizer

    def remove_organizer(self, cpf):
        for index, organizer in enumerate(self.__organizers):
            if (organizer.cpf == cpf):
                self.__organizers.pop(index)

    def open_organizers_menu(self):
        bindings = {
            1: self.open_register_organizer,
            2: self.open_edit_organizer,
            3: self.open_remove_organizer,
            4: self.open_organizers_list,
            5: self.open_find_organizer
        }

        while True:
            option = self.view.show_organizers_menu()

            if (option == 0):
                return

            bindings[option]()

    def open_register_organizer(self):
        organizer_data = self.view.show_register_organizer()

        already_has_organizer, _ = self.get_organizer_by_cpf(organizer_data['cpf'])
        if (already_has_organizer != None):
            print('Esse CPF ja foi cadastrado!')
            return

        address_data = self.__controllers_manager.address.view.show_register_address()

        current = datetime.now()
        if (current.year - organizer_data["birthday"].year > 150):
            print('O organizador nao pode ter mais que 150 anos!')
            return

        self.add_organizer(
            organizer_data["cpf"],
            organizer_data["name"],
            organizer_data["birthday"],
            address_data["cep"],
            address_data["street"],
            address_data["number"],
            address_data["complement"]
        )

        print('Organizador adicionado!')

    def open_edit_organizer(self):
        organizer = self.open_select_organizer()
        if (organizer == None):
            return

        organizer_data = self.view.show_register_organizer(True)
        address_data = self.__controllers_manager.address.view.show_register_address()
        self.edit_organizer(
            organizer.cpf,
            organizer_data["name"],
            organizer_data["birthday"],
            address_data["cep"],
            address_data["street"],
            address_data["number"],
            address_data["complement"],
        )

        print('Organizador Editado!')

    def open_remove_organizer(self):
        organizer = self.open_select_organizer()
        if (organizer == None):
            return

        self.remove_organizer(organizer.cpf)

        print('Organizador deletado!')

    def open_organizers_list(self):
        organizers = self.get_organizers()
        self.view.show_organizers_list(organizers)

    def open_find_organizer(self):
        organizer = self.open_select_organizer()
        if (organizer == None):
            return
        
        self.view.show_organizer_details(organizer)

    def open_select_organizer(self):
        organizer = None
        while True:
            organizer_cpf = self.view.show_find_organizer()

            if organizer_cpf == None:
                return

            organizer, _ = self.get_organizer_by_cpf(organizer_cpf)

            if (organizer):
                return organizer
            else:
                print('Organizador nao encontrado')
    
    def open_select_many_organizers(self):
        organizers = []
        while True:
            organizer_cpf = self.view.show_find_organizer(True, 'Digite o CPF, 0 para sair ou -1 para finalizar selecao de organizadores: ')

            if organizer_cpf == None:
                return
            
            if (organizer_cpf == '-1'):
                return organizers

            organizer, _ = self.get_organizer_by_cpf(organizer_cpf)

            if (organizer):
                organizers.append(organizer)
            else:
                print('Organizador nao encontrado')