from datetime import datetime as date, timedelta
from core.persistance.event_store import EventStore
from models.event_model import Event
from models.participant_event_model import ParticipantEvent
from views.events_view import EventsView
from core.exceptions.already_exists_exception import AlreadyExistsException
from core.exceptions.user_exit_exception import UserExitException


class EventsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.__store = EventStore(controllers_manager)
        self.view = EventsView()

    def get_events(self):
        return self.__store.list()

    def get_event_by_title(self, title):
        return self.__store.get(title)

    def add_event(self, title, max_participants, local, datetime, organizers):
        already_has_event = self.get_event_by_title(title)

        if (already_has_event):
            raise AlreadyExistsException('Evento')

        event = Event(title, max_participants, [],
                      local, datetime, organizers)

        self.__store.add(event)

    def edit_event(self, title, max_participants, participants, local, datetime, organizers):
        event = self.get_event_by_title(title)

        event.max_participants = max_participants
        event.local = local
        event.participants = participants
        event.datetime = datetime
        event.organizers = organizers

        self.__store.update(event)

    def remove_event(self, title):
        self.__store.remove(title)

    def open_events_menu(self):
        try:
            bindings = {
                'register_event': self.open_register_event,
                'edit_event': self.open_edit_event,
                'remove_event': self.open_delete_event,
                'list_events': self.open_list_events,
                'find_event': self.open_find_event
            }

            while True:
                option = self.view.show_events_menu()
                bindings[option]()
        except UserExitException:
            return

    def open_register_event(self):
        try:
            event_data = self.view.show_register_event()
            self.view.close()

            organizers = self.__controllers_manager.organizer.open_select_many_organizers()

            local = self.__controllers_manager.local.open_select_local()

            self.add_event(
                event_data['title'],
                event_data['max_participants'],
                local,
                event_data['datetime'],
                organizers
            )

            self.view.show_message('Evento adicionado!')
        except UserExitException:
            self.view.close()
            return

    def open_edit_event(self):
        try:
            event = self.open_select_event()

            event_data = self.view.show_register_event(event.to_raw())
            self.view.close()

            organizers = self.__controllers_manager.organizer.open_select_many_organizers()

            local = self.__controllers_manager.local.open_select_local()

            self.edit_event(
                event.title,
                event_data["max_participants"],
                event.participants,
                local,
                event_data["datetime"],
                organizers
            )

            self.view.show_message('Evento editado!')
        except UserExitException:
            self.view.close()
            return

    def open_add_participant_to_event(self, event):
        try:
            current = date.now()
            if (event.datetime <= current):
                self.view.show_message('Esse evento já finalizou!')
                return

            if (len(event.participants) >= event.max_participants):
                self.view.show_message('Esse evento já esta cheio!')
                return

            user = self.__controllers_manager.user.open_select_user(
                'Cadastrar Participante')

            user_event = ParticipantEvent(event, user, None, None)
            event.participants.append(user_event)

            self.edit_event(
                event.title,
                event.max_participants,
                event.participants,
                event.local,
                event.datetime,
                event.organizers
            )

            self.view.show_message('Usuário adicionado ao evento!')
        except UserExitException:
            self.view.close()
            return

    def open_delete_event(self):
        try:
            event = self.open_select_event()
            self.remove_event(event.title)
            self.view.show_message('Evento deletado!')
        except UserExitException:
            self.view.close()
            return

    def open_list_events(self):
        events = self.get_events()

        events_data = []
        for key in events:
            event = events[key]
            events_data.append(event.to_raw())

        self.view.show_events_list(events_data)

    def open_find_event(self):
        try:
            event = self.open_select_event()

            bindings = {
                'add_participant': self.open_add_participant_to_event,
                'list_participants': self.open_participants_list,
                'list_participants_with_covid_proof': self.open_participants_with_covid_proof,
                'list_participants_without_covid_proof': self.open_participants_without_covid_proof,
                'register_entrance': self.open_register_entrance,
                'register_leave': self.open_register_leave
            }

            while True:
                option = self.view.show_event_menu(event.to_raw())
                bindings[option](event)
        except UserExitException:
            self.view.close()
            return

    def open_participants_list(self, event):
        participants_data = []

        for participant_assoc in event.participants:
            raw_participant_assoc = participant_assoc.to_raw()
            raw_participant_assoc['participant']['has_covid_proof'] = self.__controllers_manager.user.can_participant_event(
                participant_assoc.participant, event)
            participants_data.append(raw_participant_assoc)

        self.view.show_participants_list(
            'Participantes do evento', participants_data)
        self.view.close()

    def edit_participant(self, event, participant_cpf, time_entrance=None, time_leave=None):
        for index, participant_assoc in enumerate(event.participants):
            if (participant_assoc.participant.cpf == participant_cpf):
                if (time_entrance):
                    participant_assoc.time_entrance = time_entrance
                if (time_leave):
                    participant_assoc.time_leave = time_leave
                event.participants[index] = participant_assoc

        self.edit_event(
            event.title,
            event.max_participants,
            event.participants,
            event.local,
            event.datetime,
            event.organizers
        )

    def open_participants_with_covid_proof(self, event):
        participants = event.participants
        participants_with_covid_proof = []
        for participant_assoc in participants:
            participant = participant_assoc.participant

            if (
                participant.has_two_vaccines or (
                    participant.pcr_exam.date and not participant.pcr_exam.has_covid)
            ):
                participants_with_covid_proof.append(
                    participant_assoc.to_raw())

        self.view.show_participants_list(
            'Participantes com comprovação Covid', participants_with_covid_proof, True)
        self.view.close()

    def open_participants_without_covid_proof(self, event):
        participants = event.participants
        participants_without_covid_proof = []
        for participant_assoc in participants:
            participant = participant_assoc.participant
            if (
                not self.__controllers_manager.user.can_participant_event(
                    participant, event)
            ):
                participants_without_covid_proof.append(
                    participant_assoc.to_raw())

        self.view.show_participants_list(
            'Participantes sem comprovação Covid', participants_without_covid_proof, True)
        self.view.close()

    def open_register_entrance(self, event):
        try:
            user = self.__controllers_manager.user.open_select_user(
                'Cadastrar Entrada')
            self.__controllers_manager.user.view.close()

            user_is_in_event = self.__user_is_in_event(user, event)

            if (not user_is_in_event):
                self.view.show_message(
                    'Esse usuário nao esta cadastrado nesse evento!')
                return

            already_register_entrance = self.__already_register_hour_entrance(
                user, event)
            if (already_register_entrance):
                self.view.show_message('Esse usuário já esta no evento!')
                return

            if (not user.has_two_vaccines):
                if (user.pcr_exam.date == None):
                    self.view.show_message(
                        'O usuário precisa de alguma confirmação que não possui covid!')
                    return

                if (user.pcr_exam.has_covid):
                    self.view.show_message(
                        'O usuário não pode participar do evento com covid')
                    return

                final_validate = user.pcr_exam.date + timedelta(days=3)
                if event.datetime > final_validate:
                    self.view.show_message(
                        'A validade do exame do usuário acaba antes do evento ocorrer')
                    return

            valid_hour = False
            while not valid_hour:
                entrance_hour, entrance_minute = self.view.show_get_hour(
                    'Cadastrar Entrada (' + event.datetime.strftime('%d/%m/%Y %H:%M') + ')')
                self.view.close()
                entrance_date = date(event.datetime.year, event.datetime.month,
                                     event.datetime.day, entrance_hour, entrance_minute)

                if (entrance_date >= event.datetime):
                    valid_hour = True
                else:
                    self.view.show_message(
                        'O horário de entrada deve ser posterior ou igual ao horário do evento')

            self.edit_participant(event, user.cpf, entrance_date)
        except UserExitException:
            return

    def open_register_leave(self, event):
        try:
            user = self.__controllers_manager.user.open_select_user(
                'Cadastrar Saída')
            self.__controllers_manager.user.view.close()

            user_is_in_event = self.__user_is_in_event(user, event)

            if (not user_is_in_event):
                self.view.show_message(
                    'Esse usuário não esta cadastrado nesse evento!')
                return

            register_entrance = self.__already_register_hour_entrance(
                user, event)
            if (not register_entrance):
                self.view.show_message(
                    'Esse usuário não entrou no evento para sair!')
                return

            already_register_leave = self.__already_register_hour_leave(
                user, event)
            if (already_register_leave):
                self.view.show_message('Esse usuário ja saiu do evento!')
                return

            valid_hour = False
            leave_date = None
            entrance_hour = self.__get_participant_assoc_hour_entrance(
                user, event)
            while not valid_hour:
                leave_hour, leave_minute = self.view.show_get_hour(
                    'Cadastrar Saída')
                self.view.close()
                leave_date = date(event.datetime.year, event.datetime.month,
                                  event.datetime.day, leave_hour, leave_minute)

                if (leave_date >= entrance_hour):
                    valid_hour = True
                else:
                    self.view.show_message(
                        'O horário de saída deve ser posterior ou igual o horário de entrada')

            self.edit_participant(event, user.cpf, None, leave_date)
        except UserExitException:
            return

    def __user_is_in_event(self, user, event):
        for participant_assoc in event.participants:
            if (participant_assoc.participant.cpf == user.cpf):
                return True
        return False

    def __get_participant_assoc_hour_entrance(self, user, event):
        for participant_assoc in event.participants:
            if (participant_assoc.participant.cpf == user.cpf):
                return participant_assoc.time_entrance
        return False

    def __already_register_hour_entrance(self, user, event):
        for participant_assoc in event.participants:
            if (participant_assoc.participant.cpf == user.cpf):
                return bool(participant_assoc.time_entrance)
        return False

    def __already_register_hour_leave(self, user, event):
        for participant_assoc in event.participants:
            if (participant_assoc.participant.cpf == user.cpf):
                return bool(participant_assoc.time_leave)
        return False

    def reflect_user_edit(self, user):
        events = self.__store.list()
        for key in events:
            event = events[key]
            for participant_index, participant_assoc in enumerate(event.participants):
                if (participant_assoc.participant.cpf == user.cpf):
                    event.participants[participant_index].participant = user
                    self.edit_event(
                        event.title,
                        event.max_participants,
                        event.participants,
                        event.local,
                        event.datetime,
                        event.organizers
                    )

    def open_select_event(self):
        while True:
            events = self.get_events()
            events_raw = []
            for key in events:
                event = events[key]
                events_raw.append(event.to_raw())

            input_find = self.view.show_find_event(events_raw)
            self.view.close()

            event = self.get_event_by_title(input_find['event'])

            if (event):
                return event
            else:
                self.view.show_message('Evento não encontrado!')
