from rest_framework.views import exception_handler  # Importa a função exception_handler do módulo rest_framework.views

# Define uma função chamada app_exception_handler que substitui o manipulador de exceções padrão do Django REST framework
def app_exception_handler(exc, context):
    # Chama o manipulador de exceções padrão do REST framework para obter a resposta de erro padrão
    response = exception_handler(exc, context)

    # Adiciona o código de status HTTP à resposta, caso exista
    if response is not None:
        response.data['success'] = False  # Adiciona um campo 'success' à resposta e define como False
        full_messages = []  # Cria uma lista para armazenar mensagens de erro detalhadas
        response.data['errors'] = {}  # Cria um dicionário para armazenar erros detalhados

        # Verifica se a exceção possui um atributo 'values', indicando detalhes específicos
        if hasattr(exc.detail, 'values'):
            # Itera sobre os valores do detalhe da exceção
            for value in list(exc.detail.items()):
                # Verifica se o valor é uma string
                if type(value) == str:
                    full_messages.append(value)  # Adiciona a string à lista de mensagens detalhadas
                # Verifica se o valor é uma tupla
                elif type(value) == tuple:
                    # Ignora certos campos que não devem ser incluídos na resposta
                    if value[0] == 'errors' or value[0] == 'success':
                        continue
                    response.data['errors'][value[0]] = str(value[1][0])  # Adiciona o erro ao dicionário de erros
                    full_messages.append('%s -> %s' % (value[0], str(value[1][0])))  # Adiciona à lista de mensagens detalhadas
            response.data['full_messages'] = full_messages  # Adiciona a lista de mensagens detalhadas à resposta
        else:
            # Caso não haja detalhes específicos, adiciona uma mensagem padrão à resposta
            response.data['full_messages'] = ['something went wrong']
            response.data['errors'] = exc.detail  # Adiciona detalhes da exceção ao dicionário de erros

    return response  # Retorna a resposta final com informações extras
