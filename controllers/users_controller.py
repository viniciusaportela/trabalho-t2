from datetime import timedelta
from core.exceptions.already_exists_exception import AlreadyExistsException
from core.exceptions.empty_store_exception import EmptyStoreException
from core.exceptions.not_exists_exception import NotExistsException
from core.exceptions.user_exit_exception import UserExitException
from core.persistance.participant_store import ParticipantStore
from models.pcr_exam_model import PCRExam
from views.user_view import UserView
from models.participant_model import Participant


class UsersController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.store = ParticipantStore()
        self.view = UserView()

    def get_users(self):
        return self.store.list()

    def get_user_by_cpf(self, cpf, silent_on_error=False):
        user = self.store.get(cpf)

        if (user == None and not silent_on_error):
            raise NotExistsException('usuário')

        return user

    def add_user(self, cpf, name, birthday, cep, street, number, complement, has_two_vaccines=None, has_covid=None, pcr_exam_date=None):
        already_has_user = self.get_user_by_cpf(cpf, silent_on_error=True)

        if (already_has_user):
            raise(AlreadyExistsException('participante'))

        user = Participant(cpf, name, birthday, cep, street, number,
                           complement, has_two_vaccines, has_covid, pcr_exam_date)
        self.store.add(user)

    def edit_user(self, cpf, name, birthday, cep, street, number, complement, has_two_vaccines=None, has_covid=None, pcr_exam_date=None):
        user = self.get_user_by_cpf(cpf)

        user.name = name
        user.birthday = birthday
        user.address.cep = cep
        user.address.street = street
        user.address.number = number
        user.address.complement = complement
        user.has_two_vaccines = has_two_vaccines

        if (has_covid != None and pcr_exam_date != None):
            user.pcr_exam = PCRExam(has_covid, pcr_exam_date)

        self.store.update(user)

        self.__controllers_manager.event.reflect_user_edit(user)

    def remove_user(self, cpf):
        self.get_user_by_cpf(cpf)
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

            while True:
                option = self.view.show_users_menu()
                bindings[option]()
        except UserExitException:
            return

    def open_register_user(self):
        try:
            user_data = None
            address_data = None

            user_correct_data = False
            first_loop = True
            while not user_correct_data:
                user_data = self.view.show_user_register(remount=first_loop)
                first_loop = False

                already_has_user = self.get_user_by_cpf(
                    user_data['cpf'], silent_on_error=True)
                if (already_has_user != None):
                    self.view.show_error_message('Esse CPF ja foi cadastrado!')
                    continue

                user_correct_data = True

            self.view.close()

            address_data = self.__controllers_manager.address.view.show_register_address()
            self.__controllers_manager.address.view.close()

            self.add_user(
                user_data["cpf"],
                user_data["name"],
                user_data["birthday"],
                address_data["cep"],
                address_data["street"],
                address_data["number"],
                address_data["complement"],
                user_data['has_two_vaccines'],
                True if user_data['pcr_exam_result'] == 'positivo' else False,
                user_data['pcr_exam_date'],
            )

            self.view.show_message('Usuário adicionado!')
        except UserExitException:
            self.view.close()
            return
        except AlreadyExistsException:
            self.view.show_message('Esse CPF ja foi cadastrado!')
            self.view.close()
            return

    def can_participant_event(self, user, event):
        if (not user.has_two_vaccines):
            if (user.pcr_exam.date == None):
                return False

            if (user.pcr_exam.has_covid):
                return False

            final_validate = user.pcr_exam.date + timedelta(days=3)
            if event.datetime > final_validate:
                return False

        return True

    def open_edit_user(self):
        try:
            user = self.open_select_user()

            user_data = self.view.show_user_register(
                user.to_raw(address_str=False))
            self.view.close()

            address_data = self.__controllers_manager.address.view.show_register_address(
                user.address.to_raw())
            self.__controllers_manager.address.view.close()

            self.edit_user(
                user.cpf,
                user_data["name"],
                user_data["birthday"],
                address_data["cep"],
                address_data["street"],
                address_data["number"],
                address_data["complement"],
                user_data['has_two_vaccines'],
                True if user_data['pcr_exam_result'] == 'positivo' else False,
                user_data['pcr_exam_date'],
            )

            self.view.show_message('Usuário editado!')
        except (UserExitException, EmptyStoreException):
            self.view.close()
            return
        except (NotExistsException):
            self.view.show_message('Usuário não existe!')
            self.view.close()
            return

    def open_remove_user(self):
        try:
            user = self.open_select_user()

            self.remove_user(user.cpf)

            self.view.show_message('Usuário deletado!')
        except (UserExitException, EmptyStoreException):
            self.view.close()
            return
        except (NotExistsException):
            self.view.show_message('Usuário não existe!')
            self.view.close()
            return

    def open_user_list(self):
        users = self.get_users()

        data_users = []
        for cpf in users:
            user = self.get_user_by_cpf(cpf, silent_on_error=True)
            raw_user = user.to_raw()
            data_users.append(raw_user)

        self.view.show_user_list(data_users)
        self.view.close()

    def open_find_user(self):
        try:
            user = self.open_select_user()

            self.view.show_user_details(user.to_raw())
        except (UserExitException, EmptyStoreException):
            self.view.close()
            return

    def open_select_user(self, title='Encontrar pessoa'):
        while True:
            def get_cpf_by_option_str(str_value):
                splitted = str_value.split('(')
                return splitted[1][:-1]

            users = self.get_users()
            if (len(users.keys()) == 0):
                self.view.show_message('Não há nenhum usuário cadastrado')
                self.view.close()
                raise EmptyStoreException('usuário')

            users_raw = []
            for key in users:
                user = users[key]
                users_raw.append(user.to_raw())

            input_find = self.view.show_find_user(users_raw, title)
            cpf = get_cpf_by_option_str(input_find['user'])

            user = self.get_user_by_cpf(cpf, silent_on_error=True)

            if (user):
                return user
            else:
                self.view.show_message('Usuário não encontrado!')
