from views.locals_view import LocalsView
from models.local_model import Local


class LocalsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.__locals = []
        self.view = LocalsView()

    def get_locals(self):
        return self.__locals

    def get_local_by_name(self, name):
        for index, local in enumerate(self.__locals):
            if (local.name == name):
                return local, index
        return None, -1

    def add_local(self, name, cep, street, number, complement):
        local = Local(name, cep, street, number, complement)
        self.__locals.append(local)
    
    def edit_local(self, name, cep, street, number, complement):
        local, _ = self.get_local_by_name(name)
        
        local.address.cep = cep
        local.address.street = street
        local.address.number = number
        local.address.complement = complement

    def delete_local(self, name):
        _, index = self.get_local_by_name(name)
        self.__locals.pop(index)

    def open_locals_menu(self):
        bindings = {
            1: self.open_register_local,
            2: self.open_edit_local,
            3: self.open_remove_local,
            4: self.open_local_list,
            5: self.open_find_local
        }

        option = None
        while option != 0:
            option = self.view.show_locals_menu()

            if (option == 0):
                return

            bindings[option]()

    def open_register_local(self):
        local_data = self.view.show_register_local()
        address_data = self.__controllers_manager.address.view.show_register_address()

        self.add_local(
            local_data['name'], 
            address_data['cep'],
            address_data['street'],
            address_data['number'],
            address_data['complement']
        )

        print('Local adicionado!')

    def open_edit_local(self):
        local_name = self.view.show_find_local()
        address_data = self.__controllers_manager.address.view.show_register_address()
        self.edit_local(
            local_name, 
            address_data['cep'], 
            address_data['street'], 
            address_data['number'], 
            address_data['complement']
        )

    def open_remove_local(self):
        local_name = self.view.show_find_local()

        if (local_name == 0):
            return

        self.delete_local(local_name)

        print('Local deletado!')

    def open_local_list(self):
        locals = self.get_locals()
        self.view.show_locals_list(locals)

    def open_find_local(self):
        local = self.open_select_local()

        if (local == None):
            return

        self.view.show_local(local)
    
    def open_select_local(self):
        local = None
        while True:
            local_name = self.view.show_find_local()

            if local_name == None:
                return

            local, _ = self.get_local_by_name(local_name)

            if (local):
                return local
            else:
                print('Local nao encontrado!')