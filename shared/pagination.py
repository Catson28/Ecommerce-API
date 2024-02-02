from rest_framework.pagination import LimitOffsetPagination  # Importa a classe LimitOffsetPagination do Django REST framework

# Define uma classe de paginação personalizada chamada AppPaginator que estende LimitOffsetPagination
class AppPaginator(LimitOffsetPagination):

    # Substitui o método get_limit para definir o número máximo de itens por página
    def get_limit(self, request):
        page_size = int(request.query_params.get('page_size', 5))  # Obtém o valor de 'page_size' dos parâmetros da consulta, padrão é 5
        if page_size < 0 or page_size > 20:  # Garante que o valor de 'page_size' esteja dentro do intervalo permitido (0 a 20)
            page_size = 5  # Define um valor padrão de 5 se estiver fora do intervalo permitido

        return page_size  # Retorna o número de itens por página

    # Substitui o método get_offset para calcular o deslocamento com base na página atual e no número de itens por página
    def get_offset(self, request):
        page = int(request.query_params.get('page', 1))  # Obtém o valor de 'page' dos parâmetros da consulta, padrão é 1
        if page < 0:  # Garante que o valor de 'page' seja pelo menos 1
            page = 1
        offset = (page - 1) * self.get_limit(request)  # Calcula o deslocamento com base na página atual e no número de itens por página
        return offset  # Retorna o deslocamento

