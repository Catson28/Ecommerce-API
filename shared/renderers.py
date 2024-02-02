import json  # Importa o módulo json para manipulação de dados JSON

from rest_framework import renderers  # Importa o módulo renderers do Django REST framework
from shared.serializers import PageMetaSerializer  # Importa o serializador PageMetaSerializer do seu aplicativo (não fornecido no código)

# Define uma classe de renderização JSON personalizada chamada AppJsonRenderer
class AppJsonRenderer(renderers.JSONRenderer):
    charset = 'utf-8'  # Define o conjunto de caracteres como 'utf-8'

    # Método construtor da classe
    def __init__(self, **kwargs):
        super(AppJsonRenderer, self).__init__()
        self.resources_name = kwargs.get('resources_name', 'resources')  # Obtém o nome dos recursos da chave 'resources_name' ou usa 'resources' como padrão

    # Método para renderizar os dados em formato JSON
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Verifica se os dados são uma string ou nulos, se sim, retorna os dados como estão
        if type(data) is str or data is None:
            return data

        results = data.get('results')  # Obtém os resultados dos dados

        # Verifica se há resultados na resposta
        if results is not None:
            page_meta = PageMetaSerializer(data, context=renderer_context)  # Serializa os metadados da página usando o PageMetaSerializer

            response = {
                'success': True,
                'page_meta': page_meta.data,
                self.resources_name: results  # Adiciona os resultados à resposta usando o nome dos recursos
            }
        else:
            response = {
                'success': False,
                'full_messages': ['Unknown error']
            }
            data['success'] = True
            response = data  # Se não houver resultados, cria uma resposta de erro desconhecido

        return json.dumps(response)  # Converte a resposta para uma string JSON

