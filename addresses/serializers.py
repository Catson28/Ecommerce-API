from rest_framework import serializers  # Importa o módulo serializers do Django REST framework
from addresses.models import Address  # Importa o modelo Address do módulo addresses.models
from users.serializers import UserUsernameAndIdSerializer  # Importa o serializador UserUsernameAndIdSerializer do módulo users.serializers

# Define um serializador para o modelo Address
class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # Adiciona um campo de método personalizado chamado 'user'

    class Meta:
        model = Address  # Especifica o modelo associado a este serializador
        fields = ['id', 'first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'user']  # Lista os campos que serão incluídos na representação serializada

    def get_user(self, address):  # Define um método personalizado para obter a representação do campo 'user'
        if self.context.get('include_user', False):  # Verifica se a chave 'include_user' está presente no contexto
            return UserUsernameAndIdSerializer(address.user).data  # Serializa o usuário usando o serializador UserUsernameAndIdSerializer e retorna os dados

        return None  # Retorna None se 'include_user' for False no contexto

    def to_representation(self, instance):  # Sobrescreve o método padrão to_representation para personalizar a representação da instância
        response = super(AddressSerializer, self).to_representation(instance)  # Chama o método to_representation da classe pai para obter a representação padrão
        if response.get('user') is None:  # Remove o campo 'user' se estiver ausente ou for None
            response.pop('user')

        return response  # Retorna a representação personalizada

    def create(self, validated_data):  # Define o método create para criar uma nova instância do modelo Address
        return Address.objects.create(user=self.context.get('user'), **validated_data)  # Cria uma nova instância do modelo Address associada ao usuário fornecido no contexto e com os dados validados fornecidos
