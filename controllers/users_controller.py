from datetime import datetime, timedelta
from core.errors.already_exists_exception import AlreadyExistsException
from core.errors.not_exists_exception import NotExistsException
from core.errors.user_exit_exception import UserExitException
from core.persistance.participant_store import ParticipantStore
from views.user_view import UserView
from models.participant_model import Participant


class UsersController:
    def __init__(self, controllers_manager):
        self.__users = []
        self.__controllers_manager = controllers_manager
        self.view = UserView()
        self.store = ParticipantStore()

    def get_users(self):
        return self.store.list()

    def get_user_by_cpf(self, cpf):
        return self.store.get(cpf)

    def add_user(self, cpf, name, birthday, cep, street, number, complement, has_two_vaccines=None, has_covid=None, pcr_exam_date=None):
        already_has_user = self.get_user_by_cpf(cpf)

        if (already_has_user):
            raise(AlreadyExistsException('participante'))

        user = Participant(cpf, name, birthday, cep, street, number,
                           complement, has_two_vaccines, has_covid, pcr_exam_date)
        self.store.add(user)

    def edit_user(self, cpf, name, birthday, cep, street, number, complement):
        user = self.get_user_by_cpf(cpf)

        if (not user):
            raise(NotExistsException('participante'))

        user.name = name
        user.birthday = birthday
        user.cep = cep
        user.address.street = street
        user.address.number = number
        user.address.complement = complement

        self.store.update(cpf, user)

    def remove_user(self, cpf):
        self.store.remove(cpf)

    def set_covid_status(self, cpf, has_two_vaccines, has_covid, pcr_exam_date):
        user, index = self.get_user_by_cpf(cpf)

        user.has_two_vaccines = has_two_vaccines
        user.pcr_exam.date = pcr_exam_date
        user.pcr_exam.has_covid = has_covid

        self.__users[index] = user

    def open_user_menu(self):
        try:
            bindings = {
                'register_user': self.open_register_user,
                'edit_user': self.open_edit_user,
                'remove_user': self.open_remove_user,
                'list_users': self.open_user_list,
                'find_user': self.open_find_user
            }

            option = self.view.open_users_menu()
            bindings[option]()
        except UserExitException:
            return

    def open_register_user(self):
        try:
            user_data = self.view.show_user_register()

            already_has_user, _ = self.get_user_by_cpf(user_data['cpf'])
            if (already_has_user != None):
                self.view.show_message('Esse CPF ja foi cadastrado!')
                return

            address_data = self.__controllers_manager.address.view.show_register_address()

            self.add_user(
                user_data["cpf"],
                user_data["name"],
                user_data["birthday"],
                address_data["cep"],
                address_data["street"],
                address_data["number"],
                address_data["complement"],
                user_data['has_two_vaccines'],
                user_data['has_covid'],
                user_data['pcr_exam_date'],
            )

            self.view.show_message('Usuario adicionado!')
        except UserExitException:
            return

    def open_register_participant(self):
        user = self.open_select_user()
        if (user == None):
            return

        participant_data = self.view.show_participant_register(True)

        self.set_covid_status(
            user.cpf,
            participant_data['has_two_vaccines'],
            participant_data['has_covid'],
            participant_data['pcr_exam_date']
        )

        print('Comprovacao Covid anexada!')

    def can_participant_event(self, user, event):
        if (not user.has_two_vaccines):
            if (user.pcr_exam.date == None):
                return False

            if (user.pcr_exam.has_covid):
                return False

            final_validate = user.pcr_exam.date + timedelta(days=3)
            if event.datetime < final_validate:
                return False

        return True

    def open_edit_user(self):
        user = self.open_select_user()
        if (user == None):
            return

        user_data = self.view.show_user_register(True)
        address_data = self.__controllers_manager.address.view.show_register_address()
        self.edit_user(
            user.cpf,
            user_data["name"],
            user_data["birthday"],
            address_data["cep"],
            address_data["street"],
            address_data["number"],
            address_data["complement"],
        )

        print('Usuario Editado!')

    def open_remove_user(self):
        user = self.open_select_user()
        if (user == None):
            return

        self.remove_user(user.cpf)

        print('Usuario deletado!')

    def open_user_list(self):
        users = self.get_users()
        self.view.show_user_list(users)

    def open_find_user(self):
        user = self.open_select_user()
        if (user == None):
            return

        self.view.show_user_details(user)

    def open_select_user(self):
        user = None
        while True:
            user_cpf = self.view.show_find_user()

            if user_cpf == None:
                return

            user, _ = self.get_user_by_cpf(user_cpf)

            if (user):
                return user
            else:
                print('Usuario nao encontrado')
