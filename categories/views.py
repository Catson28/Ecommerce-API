from rest_framework import generics  # Importa módulos do Django REST framework

from categories.models import Category  # Importa o modelo Category do aplicativo categories
from categories.serializers import CategoryIdAndNameSerializer  # Importa o serializador CategoryIdAndNameSerializer do aplicativo categories
from shared.renderers import AppJsonRenderer  # Importa o renderizador AppJsonRenderer do módulo shared
from users.authentication import IsAdminOrReadOnly  # Importa a classe de permissão IsAdminOrReadOnly

# Define uma classe de visualização chamada CategoryListCreateView que estende generics.ListCreateAPIView
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryIdAndNameSerializer  # Define a classe do serializador como CategoryIdAndNameSerializer
    permission_classes = [IsAdminOrReadOnly, ]  # Define as classes de permissão, permitindo acesso de leitura apenas para usuários não autenticados

    def get_queryset(self):
        return Category.objects.all()  # Obtém todos os objetos do modelo Category

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        serializer_context['include_urls'] = True
        page = self.paginate_queryset(self.get_queryset())  # Pagina o conjunto de consultas
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)  # Serializa os dados paginados
        return self.get_paginated_response(serialized_data.data)  # Retorna a resposta paginada

    def get_serializer_context(self):
        serializer_context = super(CategoryListCreateView, self).get_serializer_context()  # Obtém o contexto do serializador
        serializer_context['include_urls'] = True
        serializer_context['request'] = self.request
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(CategoryListCreateView, self).get_renderer_context()  # Obtém o contexto do renderizador
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='tags')]  # Retorna a lista de renderizadores usando AppJsonRenderer

    def perform_create(self, serializer):
        super(CategoryListCreateView, self).perform_create(serializer)
        data = {'success': True, 'full_messages': ['Tag created successfully']}
        serializer.data.update(data)  # Adiciona mensagens de sucesso aos dados serializados
