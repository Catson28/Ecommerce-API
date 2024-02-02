from django.conf.urls import url  # Importa o módulo url do Django

# Importa as views necessárias do módulo addresses.views e products.views
from addresses.views import AddressListView
from products.views import ProductListView, ProductDetailsView

app_name = 'addresses'  # Define um namespace para as URLs deste aplicativo
urlpatterns = [
    url(r'^addresses$', AddressListView.as_view(), name='address_list'),  # Define uma URL padrão para a lista de endereços
    # url(r'^users/addresses$', AddressListView.as_view(), name='address_list'),  # Exemplo comentado de uma URL alternativa para a lista de endereços
]
