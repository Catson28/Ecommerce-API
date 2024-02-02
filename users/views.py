# Create your views here.
from rest_framework import status  # Importa o módulo status do Django REST framework
from rest_framework.permissions import AllowAny  # Importa a permissão AllowAny do Django REST framework
from rest_framework.response import Response  # Importa a classe Response do Django REST framework
from rest_framework.views import APIView  # Importa a classe APIView do Django REST framework

from users.serializers import RegistrationSerializer  # Importa o serializador RegistrationSerializer do aplicativo users

# Define uma classe de visualização chamada Register que herda de APIView
class Register(APIView):
    permission_classes = (AllowAny,)  # Define as permissões permitidas para qualquer usuário
    serializer_class = RegistrationSerializer  # Define a classe do serializador a ser usada

    def post(self, request):
        # user = user.intersect('email', 'username', 'password', 'password_confirmation')
        context = {'request': request}  # Cria um contexto para o serializador
        serialized = self.serializer_class(data=request.data, context=context)  # Cria uma instância do serializador com os dados da requisição e o contexto
        serialized.is_valid(raise_exception=True)  # Valida os dados do serializador; se inválido, gera uma exceção
        serialized.save()  # Salva os dados do serializador criando um novo usuário
        data = {'success': True}  # Cria um dicionário de dados com uma chave de sucesso
        data.update(serialized.data)  # Adiciona os dados serializados ao dicionário de dados
        return Response(data=data, status=status.HTTP_201_CREATED)  # Retorna uma resposta com os dados e o código de status 201 (Created)
