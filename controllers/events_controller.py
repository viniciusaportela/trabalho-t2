from datetime import datetime as date, timedelta
from models.event_model import Event
from models.participant_event_model import ParticipantEvent
from views.events_view import EventsView


class EventsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.__events = []
        self.view = EventsView()

    def get_events(self):
        return self.__events

    def get_event_by_title(self, title):
        for index, event in enumerate(self.__events):
            if event.title == title:
                return event, index
        return None, -1

    def add_event(self, title, max_participants, local, datetime_str, organizers):
        already_has_event, _ = self.get_event_by_title(title)

        if (already_has_event):
            return False, 'Esse evento ja existe!'
        
        date_time_split = datetime_str.split(' ')
        date_split = date_time_split[0].split('/')
        hour_split = date_time_split[1].split(':')

        datetime_str = date(
            int(date_split[2]),
            int(date_split[1]),
            int(date_split[0]),
            int(hour_split[0]),
            int(hour_split[1])
        )

        event = Event(title, max_participants, [], local, datetime_str, organizers)

        self.__events.append(event)

        return True, ''

    def edit_event(self, title, max_participants, participants, local, datetime, organizers):
        event, _ = self.get_event_by_title(title)

        event.max_participants = max_participants
        event.local = local
        event.participants = participants
        event.organizers = organizers

        date_time_split = datetime.split(' ')
        date_split = date_time_split[0].split('/')
        hour_split = date_time_split[1].split(':')
        datetime_final = date(
            int(date_split[2]),
            int(date_split[1]),
            int(date_split[0]),
            int(hour_split[0]),
            int(hour_split[1])
        )
        event.datetime = datetime_final
    
    def remove_event(self, title):
        _, index = self.get_event_by_title(title)
        self.__events.pop(index)

    def open_events_menu(self):
        bindings = {
            1: self.open_register_event,
            2: self.open_edit_event,
            3: self.open_delete_event,
            4: self.open_list_events,
            5: self.open_find_event
        }

        while True:
            option = self.view.show_events_menu()

            if (option == 0):
                return

            bindings[option]()

    def open_register_event(self):
        event_data = self.view.show_register_event()
        print('Selecione os organizadores:')
        organizers = self.__controllers_manager.organizer.open_select_many_organizers()
        if (organizers == None):
            return
        if (len(organizers) == 0):
            print('Voce deveria escolher ao menos um organizador!')
            return

        local = self.__controllers_manager.local.open_select_local()

        self.add_event(
            event_data['name'],
            event_data['max_participants'],
            local,
            event_data['event_date'],
            organizers
        )

        print('Evento adicionado!')

    def open_edit_event(self):
        event = self.open_select_event()
        if (event == None):
            return

        event_data = self.view.show_register_event(True)
        print('Selecione os organizadores:')
        organizers = self.__controllers_manager.organizer.open_select_many_organizers()
        if (organizers == None):
            return
        if (len(organizers) == 0):
            print('Voce deveria escolher ao menos um organizador!')
            return
        local = self.__controllers_manager.local.open_select_local()

        self.edit_event(
            event.title,
            event_data["max_participants"],
            event.participants,
            local,
            event_data["event_date"],
            organizers
        )

        print('Evento editado!')

    def open_add_participant_to_event(self, event):
        print('-----------= Cadastrar pessoa em evento =-----------')

        current = date.now()
        if (event.datetime <= current):
            print('Esse evento ja finalizou!')
            return

        if (len(event.participants) >= event.max_participants):
            print('Esse evento ja esta cheio!')
            return

        user = self.__controllers_manager.user.open_select_user()
        if (user == None):
            return

        user_event = ParticipantEvent(event, user, None, None)

        event.participants.append(user_event)

        self.edit_event(
            event.title,
            event.max_participants,
            event.participants,
            event.local,
            event.datetime.strftime('%d/%m/%Y %H:%M'),
            event.organizers
        )

        print('Usuario adicionado ao evento!')

    def open_delete_event(self):
        event = self.open_select_event()
        if (event == None):
            return

        self.remove_event(event.title)

        print('Evento deletado!')

    def open_list_events(self):
        events = self.get_events()
        self.view.show_events_list(events)

    def open_find_event(self):
        event = self.open_select_event()
        if (event == None):
            return

        bindings = {
            1: self.open_add_participant_to_event,
            2: self.open_participants_list,
            3: self.open_participants_with_covid_proof,
            4: self.open_participants_without_covid_proof,
            5: self.open_register_entrance,
            6: self.open_register_leave
        }

        while True:
            option = self.view.show_event_menu(event)

            if (option == 0):
                return

            bindings[option](event)

    def open_participants_list(self, event):
        participants = []

        for participant_assoc in event.participants:
            participants.append(participant_assoc)

        self.view.show_participants_list(participants)

    def edit_participant(self, event, participant_cpf, time_entrance = None, time_leave = None):
        for index, participant_assoc in enumerate(event.participants):
            if (participant_assoc.participant.cpf == participant_cpf):
                if (time_entrance):
                    participant_assoc.time_entrance = time_entrance
                if (time_leave):
                    participant_assoc.time_leave = time_leave
                event.participants[index] = participant_assoc

    def open_participants_with_covid_proof(self, event):
        participants = event.participants
        participants_with_covid_proof = []
        for participant_assoc in participants:
            participant = participant_assoc.participant

            if (
                participant.has_two_vaccines or (participant.pcr_exam.date and not participant.pcr_exam.has_covid)
            ):
                participants_with_covid_proof.append(participant_assoc)
        
        self.view.show_participants_list(participants_with_covid_proof, '-----------= Participantes com comprovacao Covid =-----------')

    def open_participants_without_covid_proof(self, event):
        participants = event.participants
        participants_without_covid_proof = []
        for participant_assoc in participants:
            participant = participant_assoc.participant
            if (
                not self.__controllers_manager.user.can_participant_event(participant, event)
            ):
                participants_without_covid_proof.append(participant_assoc)
        
        self.view.show_participants_list(participants_without_covid_proof, '-----------= Participantes sem comprovacao Covid =-----------')

    def open_register_entrance(self, event):
        print('-----------= Cadastrar Entrada =-----------')
        user = self.__controllers_manager.user.open_select_user()
        if (user == None):
            return
        
        user_is_in_event = self.__user_is_in_event(user, event)

        if (not user_is_in_event):
            print('Esse usuario nao esta cadastrado nesse evento!')
            return
        
        already_register_entrance = self.__already_register_hour_entrance(user, event)
        if (already_register_entrance):
            print('Esse usuario ja esta no evento!')
            return
        
        if (not user.has_two_vaccines):
            if (user.pcr_exam.date == None):
                print('O usuario precisa de alguma confirmacao que nao possui covid!')
                return

            if (user['has_covid']):
                    print('O usuario nao pode participar do evento com covid')
                    return
            
            final_validate = user['pcr_exam_date'] + timedelta(days=3)
            if event.datetime < final_validate:
                print('A validade do exame do usuario acaba antes do evento ocorrer')
                return

        valid_hour = False
        while not valid_hour:
            entrance_hour, entrance_minute = self.view.get_hour()
            entrance_date = date(event.datetime.year, event.datetime.month, event.datetime.day, entrance_hour, entrance_minute)

            if (entrance_date >= event.datetime):
                valid_hour = True
            else:
                print('O horario de entrada deve ser posterior ou igual ao horario do evento')
        
        self.edit_participant(event, user.cpf, entrance_date)

    def open_register_leave(self, event):
        print('-----------= Cadastrar Saida =-----------')
        user = self.__controllers_manager.user.open_select_user()
        if (user == None):
            return
        
        user_is_in_event = self.__user_is_in_event(user, event)

        if (not user_is_in_event):
            print('Esse usuario nao esta cadastrado nesse evento!')
            return

        register_entrance = self.__already_register_hour_entrance(user, event)
        if (not register_entrance):
            print('Esse usuario nao entrou no evento para sair!')
            return
        
        already_register_leave = self.__already_register_hour_leave(user, event)
        if (already_register_leave):
            print('Esse usuario ja saiu do evento!')
            return
        
        valid_hour = False
        leave_date = None
        entrance_hour = self.__get_participant_assoc_hour_entrance(user, event)
        while not valid_hour:
            leave_hour, leave_minute = self.view.get_hour()
            leave_date = date(event.datetime.year, event.datetime.month, event.datetime.day, leave_hour, leave_minute)

            if (leave_date >= entrance_hour):
                valid_hour = True
            else:
                print('O horario de saida deve ser posterior ou igual o horario de entrada')
        
        self.edit_participant(event, user.cpf, None, leave_date)

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

    def update_user_reference(self, user):
        for event_index, event in enumerate(self.__events):
            for participant_index, participant_assoc in enumerate(event.participants):
                if (participant_assoc.participant.cpf == user.cpf):
                    self.__events[event_index].participants[participant_index].participant = user

    def open_select_event(self):
        while True:
            event_title = self.view.show_find_event()

            if event_title == None:
                return

            event, _ = self.get_event_by_title(event_title)

            if (event):
                return event
            else:
                print('Evento nao encontrado!')
