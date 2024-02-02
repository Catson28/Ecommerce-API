from rest_framework.validators import UniqueValidator  # Importa o validador UniqueValidator do Django REST framework
from rest_framework import serializers  # Importa o módulo serializers do Django REST framework

from users.models import AppUser  # Importa o modelo AppUser do aplicativo users

# Define um serializador chamado UserUsernameAndIdSerializer que herda de ModelSerializer
class UserUsernameAndIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser  # Define o modelo associado ao serializador
        fields = ['id', 'username']  # Define os campos a serem incluídos no serializador

# Define um serializador chamado RegistrationSerializer que herda de ModelSerializer
class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  # Define um campo de caractere obrigatório para o primeiro nome
    last_name = serializers.CharField(required=True)  # Define um campo de caractere obrigatório para o último nome
    username = serializers.CharField(validators=[UniqueValidator(queryset=AppUser.objects.all())])  # Define um campo de caractere para o nome de usuário com validação de unicidade
    email = serializers.CharField(validators=[UniqueValidator(queryset=AppUser.objects.all())])  # Define um campo de caractere para o e-mail com validação de unicidade
    password = serializers.CharField(write_only=True)  # Define um campo de caractere (senha) que não será retornado na resposta
    password_confirmation = serializers.CharField(write_only=True)  # Define um campo de caractere (confirmação de senha) que não será retornado na resposta

    def create(self, validated_data):
        validated_data.pop('password_confirmation')  # Remove a confirmação de senha dos dados validados
        user = AppUser.objects.create_user(**validated_data)  # Cria um usuário usando o método create_user do modelo AppUser
        return user

    def validate_password(self, password):
        password_confirmation = self.context.get('request').data.get('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError('password and password confirmation do not match')  # Valida se a senha e a confirmação de senha coincidem
        return password

    class Meta:
        model = AppUser  # Define o modelo associado ao serializador
        fields = ['first_name', 'last_name', 'username', 'email', 'password_confirmation', 'password']  # Define os campos a serem incluídos no serializador
