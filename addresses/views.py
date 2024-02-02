from rest_framework import generics, status  # Importa módulos do Django REST framework
from rest_framework.permissions import IsAuthenticated  # Importa a permissão IsAuthenticated
from rest_framework.response import Response  # Importa a classe Response

from addresses.models import Address  # Importa o modelo Address do aplicativo addresses
from addresses.serializers import AddressSerializer  # Importa o serializador AddressSerializer do aplicativo addresses
from comments.serializers import CommentSerializer  # Importa o serializador CommentSerializer do aplicativo comments
from products.models import Product  # Importa o modelo Product do aplicativo products
from shared.renderers import AppJsonRenderer  # Importa o renderizador AppJsonRenderer do módulo shared

# Define uma classe de visualização chamada AddressListView que estende generics.ListCreateAPIView
class AddressListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer  # Define a classe do serializador como AddressSerializer
    permission_classes = (IsAuthenticated,)  # Define as classes de permissão, permitindo apenas usuários autenticados

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)  # Obtém o conjunto de consultas filtrando os endereços pelo usuário autenticado

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()  # Obtém o contexto do serializador
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())  # Pagina o conjunto de consultas
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)  # Serializa os dados paginados
        return self.get_paginated_response(serialized_data.data)  # Retorna a resposta paginada

    def get_serializer_context(self):
        serializer_context = super(AddressListView, self).get_serializer_context()  # Obtém o contexto do serializador
        serializer_context['include_user'] = False  # Define 'include_user' como False no contexto do serializador
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(AddressListView, self).get_renderer_context()  # Obtém o contexto do renderizador
        renderer_context['paginator'] = self.paginator  # Define o paginador no contexto do renderizador
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='addresses')]  # Retorna a lista de renderizadores usando AppJsonRenderer

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
            'include_user': True,
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        data = {'full_messages': ['Address created successfully']}
        data.update(AddressSerializer(address, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)
