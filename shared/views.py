# Create your views here.
from rest_framework import generics

class ResourceListView(generics.ListAPIView):
    # Vista base para listagem de recursos

    def list(self, request, *args, **kwargs):
        # Método para processar requisições GET e retornar a lista paginada de recursos
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        # Método para obter o contexto do serializador
        serializer_context = super(ResourceListView, self).get_serializer_context()
        serializer_context['include_user'] = True
        serializer_context['include_product'] = False
        return serializer_context

    def get_renderer_context(self):
        # Método para obter o contexto do renderizador
        renderer_context = super(ResourceListView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context
