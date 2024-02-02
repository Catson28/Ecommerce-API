import os  # Importa o módulo os para manipulação de sistema de arquivos
from random import choice  # Importa a função choice do módulo random para gerar caracteres aleatórios
from string import ascii_lowercase  # Importa a string ascii_lowercase para gerar caracteres aleatórios

from rest_framework import serializers  # Importa o módulo serializers do Django REST framework

from categories.models import Category  # Importa o modelo Category do aplicativo categories
from fileuploads.models import CategoryImage  # Importa o modelo CategoryImage do aplicativo fileuploads

# Define um serializador chamado CategoryIdAndNameSerializer que herda de serializers.ModelSerializer
class CategoryIdAndNameSerializer(serializers.ModelSerializer):
    '''
    image = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False)
    )
    '''

    # Define um campo SerializerMethodField chamado image_urls
    image_urls = serializers.SerializerMethodField()

    # Método para obter as URLs das imagens associadas à categoria
    def get_image_urls(self, category):
        if self.context.get('include_urls', False):
            return [x.file_path for x in category.images.all()]

        return None

    # Sobrescreve o método to_representation para personalizar a representação do objeto
    def to_representation(self, instance):
        response = super(CategoryIdAndNameSerializer, self).to_representation(instance)
        if response.get('image_urls') is None:
            response.pop('image_urls')

        return response

    # Sobrescreve o método create para customizar a lógica de criação da categoria
    def create(self, validated_data):

        request = self.context['request']
        images = request.data.get('images')
        if images is not None:
            images = list(images)

        # Obtém o diretório para salvar as imagens
        dir = os.path.join(os.getcwd(), 'static', 'images', 'categories')
        file_name = "".join(choice(ascii_lowercase) for i in range(16)) + ".png"

        # Cria o diretório se não existir
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Chama o método create da classe pai para criar a categoria
        category = super(CategoryIdAndNameSerializer, self).create(validated_data)
        
        # Verifica se há imagens para processar
        if images is not None:
            for image in images:
                file_path = os.path.join(dir, file_name + '.png')
                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                        # Cria uma instância de CategoryImage associada à categoria
                        CategoryImage.objects.create(
                            file_name=file_name,
                            original_name=image.name,
                            file_length=image.size,
                            category=category,
                            file_path=file_path.replace(os.getcwd(), '').replace('\\', '/')
                        )

        return category

    class Meta:
        model = Category  # Define o modelo associado a este serializador como Category
        fields = ['id', 'name', 'image_urls']  # Define os campos que serão serializados
