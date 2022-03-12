class LocalsView:
    def show_locals_menu(self):
        while True:
            print('-----------= Menu Locais =-----------')
            print('1 - Cadastrar Local')
            print('2 - Editar Local')
            print('3 - Remover Local')
            print('4 - Listar Locais')
            print('5 - Procurar Local')
            print('0 - Voltar')
            option = int(input('Por favor insira uma opcao: ').strip() or '-1')
            if (option >= 0 and option <= 6):
                return option
            else:
                print('Escolha uma opcao valida!')

    def show_register_local(self):
        print('-----------= Cadastrar Local =-----------')
        name = input('Nome: ')

        return { "name": name }

    def show_find_local(self):
        print('-----------= Procurar Local =-----------')
        local = input('Digite o nome do local ou 0 para sair: ')

        if (local == '0'):
            return None
        
        return local
    
    def show_locals_list(self, locals):
        print('-----------= Locais =-----------')

        for index, local in enumerate(locals):
            print(str(index +  1) + ' - ' + local.name + ' (' + local.address.cep + ')')
        
        input('Aperte enter para sair... ')

    def show_local(self, local):
        print('-----------= Local =-----------')
        print('Nome: ' + local.name)
        print('Endereco: ' + local.address.cep + ', ' + local.address.street + ', n. ' + local.address.number + ', ' + local.address.complement)

        input('Aperte enter para sair... ')