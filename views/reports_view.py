class ReportsView:
    def show_reports_menu(self):
        while True:
            print('-----------= Menu Relatorios =-----------')
            print('1 - Eventos a realizar')
            print('2 - Ranking de eventos por numero de participantes')
            print('3 - Eventos ja realizados')
            print('0 - Voltar')
            
            option = int(input('Por favor insira uma opcao: ').strip() or '-1')
            
            if (option >= 0 and option <= 3):
                return option
            else:
                print('Escolha uma opcao valida!')

    def show_report_events(self, events, header = None, with_participants = None):
        if (header):
            print(header)
        else:
            print('-----------= Eventos =-----------')

        for index, event in enumerate(events):
            print(
                str(index + 1) + 
                ' - ' + 
                event.title + 
                ' (' + 
                event.local.name +
                ')' +
                ' - ' +
                event.datetime.strftime('%d/%m/%Y %H:%M') +
                ((' - ' + str(len(event.participants)) + ' participantes') if with_participants else '')
            )
        
        input('Aperte enter para sair... ')