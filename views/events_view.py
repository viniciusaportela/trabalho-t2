from utils.date_validator import validate_datetime, validate_time
from utils.recurring_ask import recurring_ask


class EventsView:
    def show_events_menu(self):
        while True:
            print('-----------= Eventos =-----------')
            print('1 - Cadastrar evento')
            print('2 - Editar evento')
            print('3 - Deletar evento')
            print('4 - Listar eventos')
            print('5 - Procurar evento / Manipular evento')
            print('0 - Voltar')

            option = int(input('Selecione uma das opcoes: ').strip() or '-1')

            if (option >= 0 and option <= 5):
                return option
            else:
                print('Escolha uma opcao valida!')

    def show_register_event(self, edit_mode = False):
        print('-----------= Editar Evento =-----------' if edit_mode else '-----------= Registrar Evento =-----------')
        name = None
        if (not edit_mode):
            name = input('Nome: ')
        
        def ask_max_participants():
            max_participants = input('Max Participantes: ')
            if (not max_participants.isnumeric()):
                return None
            return int(max_participants)
        max_participants = recurring_ask(ask_max_participants)
        
        def ask_datetime():
            datetime_raw = input('Data e Hora (dia/mes/ano hora:minuto): ')
            is_date_valid = validate_datetime(datetime_raw)
            if (not is_date_valid):
                return None
            return datetime_raw
        datetime_raw = recurring_ask(ask_datetime)

        return { "name": name, "max_participants": max_participants, "event_date": datetime_raw }

    def show_events_list(self, events):
        print('-----------= Eventos =-----------')

        for index, event in enumerate(events):
            print(str(index +  1) + ' - ' + event.title + ' (' + event.local.name + ' - ' + event.datetime.strftime('%d/%m/%Y %H:%M') + ')')
        
        input('Aperte enter para sair... ')

    def show_event_menu(self, event):
        while True:
            print('-----------= Evento =-----------')
            print('Nome: ' + event.title)
            print('Participantes: ' + str(len(event.participants)) + '/' + str(event.max_participants))
            print('Data: ' + event.datetime.strftime('%d/%m/%Y %H:%M'))
            print('Local: ' + event.local.name)
            print('Organizadores: ' + self.__get_organizers_str(event))
            print('')
            print('1 - Cadastrar Participante')
            print('2 - Listar Participantes')
            print('3 - Listar Participantes com comprovacao Covid')
            print('4 - Listar Participantes sem comprovacao Covid')
            print('5 - Registrar entrada')
            print('6 - Registrar saida')
            print('0 - Sair')

            option = int(input('Selecione uma das opcoes: ').strip() or '-1')

            if (option >= 0 and option <= 6):
                return option
            else:
                print('Escolha uma opcao valida!')
    
    def __get_organizers_str(self, event):
        str = ''
        for index, organizer in enumerate(event.organizers):
            str += organizer.name + ' (' + organizer.cpf + ')' + (', ' if index != len(event.organizers) - 1 else '')
        return str

    def show_find_event(self, headless = False):
        if (not headless):
            print('-----------= Procurar Evento =-----------')
        local_name = input('Digite o nome do evento ou 0 para sair: ')

        if (local_name == '0'):
            return None

        return local_name

    def show_participants_list(self, participants_assoc, custom_header = None):
        if (custom_header):
            print(custom_header)
        else:
            print('-----------= Participantes =-----------')

        for index, participant_assoc in enumerate(participants_assoc):
            participant = participant_assoc.participant

            def get_date_formatted(datetime):
                if (datetime):
                    return datetime.strftime('%H:%M')
                else:
                    return 'x'

            print(
                str(index + 1) + 
                ' - ' + 
                participant.name + 
                ' (' + 
                participant.cpf + 
                ')' + 
                (
                    (' (' + get_date_formatted(participant_assoc.time_entrance) + ' -> ' + get_date_formatted(participant_assoc.time_leave) + ')') if (participant_assoc.time_entrance or participant_assoc.time_leave) else ''
                )
            )
        
        input('Aperte enter para sair... ')

    def get_hour(self):
        def ask_hour():
            date_raw = input('Horario de Entrada (H:m): ')
            is_date_valid = validate_time(date_raw)
            if (not is_date_valid):
                return None
            return date_raw
        date_raw = recurring_ask(ask_hour)
        date_raw_split = date_raw.split(':')

        hour = int(date_raw_split[0])
        minute = int(date_raw_split[1])

        return hour, minute

