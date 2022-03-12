def recurring_ask(ask):
    is_to_retry = True
    response = None
    while is_to_retry:
        response = ask()
        if (response != None):
            is_to_retry = False
        else:
            print('Insira uma resposta valida!')
    return response
    