from rest_framework import serializers  # Importa o módulo serializers do Django REST framework

from addresses.serializers import AddressSerializer  # Importa o serializador AddressSerializer do aplicativo addresses
from orders.models import Order, OrderItem  # Importa os modelos Order e OrderItem do aplicativo orders
from users.serializers import UserUsernameAndIdSerializer  # Importa o serializador UserUsernameAndIdSerializer do aplicativo users

# Define um novo serializador chamado OrderItemSerializer que herda de serializers.ModelSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # Define um campo de inteiro para o ID
    quantity = serializers.IntegerField()  # Define um campo de inteiro para a quantidade

    class Meta:
        model = OrderItem  # Define o modelo associado a este serializador como OrderItem
        fields = ['id', 'price', 'quantity']  # Define os campos que serão serializados

# Define um novo serializador chamado OrderSerializer que herda de serializers.ModelSerializer
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o usuário
    order_status = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o status do pedido
    total = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o total do pedido
    tracking_number = serializers.CharField(read_only=True)  # Define um campo de caractere somente leitura para o número de rastreamento
    order_items = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para os itens do pedido
    address = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para o endereço do pedido
    order_items_count = serializers.SerializerMethodField()  # Define um campo SerializerMethodField para a contagem de itens do pedido

    class Meta:
        model = Order  # Define o modelo associado a este serializador como Order
        fields = ['id', 'user', 'tracking_number', 'order_status', 'total', 'order_items_count', 'order_items',
                  'address']  # Define os campos que serão serializados

    # Método para obter a representação do usuário associado ao pedido
    def get_user(self, order):
        if self.context.get('include_user', False):
            return UserUsernameAndIdSerializer(order.user).data
        else:
            return None

    # Sobrescreve o método to_representation para personalizar a representação do objeto
    def to_representation(self, instance):
        response = super(OrderSerializer, self).to_representation(instance)
        if response.get('order_items') is None and 'order_items' in response:
            response.pop('order_items')

        if response.get('user') is None and 'user' in response:
            response.pop('user')

        if response.get('address') is None and 'address' in response:
            response.pop('address')

        if response.get('order_items_count') is None and 'order_items_count' in response:
            response.pop('order_items_count')

        return response

    # Sobrescreve o método create para customizar a lógica de criação do pedido
    def create(self, validated_data):
        order = Order(address=self.context['address'])
        if self.context['user'] and self.context['user'].is_authenticated:
            order.user = self.context['user']
        order.save()
        return order

    # Método para obter a representação do status do pedido
    def get_order_status(self, order):
        return Order.ORDER_STATUS[order.order_status][1]

    # Método para obter o total do pedido
    def get_total(self, order):
        total = 0
        for oi in order.order_items.all():
            total += oi.price
        return total

    # Método para obter a representação do endereço associado ao pedido
    def get_address(self, order):
        address = self.context.get('address', None)
        if address is not None:
            address = AddressSerializer(address).data
            return address
        else:
            return None

    # Método para obter a representação dos itens do pedido
    def get_order_items(self, order):
        if self.context.get('include_order_items', False):
            order_items = OrderItemSerializer(order.order_items, many=True).data
            return order_items
        else:
            return None

    # Método para obter a contagem de itens do pedido
    def get_order_items_count(self, product):
        return getattr(product, 'order_items__count', None)
