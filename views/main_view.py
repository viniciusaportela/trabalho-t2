class MainView:
    def show_menu(self):
        while True:
            print('-----------= Menu =-----------')
            print('1 - Pessoas')
            print('2 - Eventos')
            print('3 - Organizadores')
            print('4 - Locais')
            print('5 - Relatorios')
            print('0 - Sair')
        
            option = int(input('Selecione uma das opcoes: ').strip() or '-1')

            if (option >= 0 and option <= 5):
                return option
            else:
                print('Escolha uma opcao valida!')