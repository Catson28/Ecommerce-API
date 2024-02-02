# Importa módulos do Django REST framework
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from comments.models import Comment  # Importa o modelo Comment do aplicativo comments
from comments.serializers import CommentSerializer  # Importa o serializador CommentSerializer do aplicativo comments
from products.models import Product  # Importa o modelo Product do aplicativo products
from shared.renderers import AppJsonRenderer  # Importa o renderizador AppJsonRenderer do módulo shared

# Importa a classe de permissão IsAdminOrOwnerOrReadOnly do módulo de autenticação dos usuários
from users.authentication import IsAdminOrOwnerOrReadOnly

# Define uma classe de visualização chamada CommentListView que estende generics.ListCreateAPIView
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer  # Define a classe do serializador como CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)  # Define as classes de permissão, permitindo acesso de leitura apenas para usuários não autenticados

    def get_queryset(self):
        return Comment.objects.filter(product__slug=self.kwargs['slug'])  # Obtém todos os comentários associados ao produto específico

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())  # Pagina o conjunto de consultas
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)  # Serializa os dados paginados
        return self.get_paginated_response(serialized_data.data)  # Retorna a resposta paginada

    def get_serializer_context(self):
        serializer_context = super(CommentListView, self).get_serializer_context()  # Obtém o contexto do serializador
        serializer_context['include_user'] = True
        serializer_context['include_product'] = False
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(CommentListView, self).get_renderer_context()  # Obtém o contexto do renderizador
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='comments')]  # Retorna a lista de renderizadores usando AppJsonRenderer

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
            'include_user': True,
            'include_product': True
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(slug=kwargs['slug'])
        serializer_context['product'] = product
        comment = serializer.save()
        data = {'full_messages': ['Comment created successfully']}
        data.update(CommentSerializer(comment, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)

# Define uma classe de visualização chamada CommentDetailsView que estende generics.RetrieveUpdateDestroyAPIView
class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer  # Define a classe do serializador como CommentSerializer
    renderer_classes = (AppJsonRenderer,)  # Define os renderizadores usados nesta visualização
    permission_classes = [IsAdminOrOwnerOrReadOnly]  # Define as classes de permissão, permitindo acesso somente a administradores ou proprietários dos comentários

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs['pk'])  # Obtém o comentário específico

    def get_serializer_context(self):
        context = super(CommentDetailsView, self).get_serializer_context()  # Obtém o contexto do serializador
        context['include_user'] = True
        context['include_product'] = True
        return context

    def destroy(self, request, *args, **kwargs):
        response = super(CommentDetailsView, self).destroy(request, args, kwargs)
        return Response({'full_messages': ['Removed comment successfully']}, status=status.HTTP_204_NO_CONTENT)
