from rest_framework import serializers, fields  # Importa módulos do Django REST framework
from comments.models import Comment  # Importa o modelo Comment do aplicativo comments
from users.serializers import UserUsernameAndIdSerializer  # Importa o serializador UserUsernameAndIdSerializer do aplicativo users

# Define um serializador chamado CommentSerializer que herda de serializers.ModelSerializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o usuário
    product = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o produto

    class Meta:
        model = Comment  # Define o modelo associado a este serializador como Comment
        fields = ['id', 'user', 'content', 'user', 'product']  # Define os campos que serão serializados

    # Método para obter a representação do produto associado ao comentário
    def get_product(self, comment):
        if self.context.get('include_product', False):
            from products.serializers import ProductElementalSerializer
            return ProductElementalSerializer(comment.product).data
        else:
            return None

    # Método para obter a representação do usuário associado ao comentário
    def get_user(self, comment):
        if self.context.get('include_user', False):
            return UserUsernameAndIdSerializer(comment.user).data
        else:
            return None

    # Sobrescreve o método to_representation para personalizar a representação do objeto
    def to_representation(self, instance):
        response = super(CommentSerializer, self).to_representation(instance)
        if response.get('product') is None:
            response.pop('product')

        if response.get('user') is None:
            response.pop('user')

        return response

    # Sobrescreve o método create para customizar a lógica de criação do comentário
    def create(self, validated_data):
        comment = Comment.objects.create(
            content=validated_data['content'],
            user=self.context['user'],
            product=self.context['product']
        )
        return comment
