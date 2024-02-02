from django.core.validators import MinValueValidator  # Importa o validador MinValueValidator do Django
from django.db import models  # Importa o módulo models do Django

# Create your models here.
from addresses.models import Address  # Importa o modelo Address do aplicativo addresses
from products.models import Product  # Importa o modelo Product do aplicativo products
from shared.models import TimestampedModel  # Importa o modelo TimestampedModel do módulo shared
from users.models import AppUser  # Importa o modelo AppUser do aplicativo users

# Define um novo modelo chamado OrderManager que herda de models.Manager
class OrderManager(models.Manager):

    # Método para verificar se um usuário comprou um produto específico
    def has_bought_product(self, product):
        Order.objects.filter(order_items__product_id=product.id)

    # Método para obter um pedido que não contenha um produto específico
    def get_order_not_containing_product(self, product):
        return Order.objects.exclude(order_items__product_id=product.id).first()

# Define um novo modelo chamado Order que herda de TimestampedModel
class Order(TimestampedModel):
    ORDERED = 0
    IN_TRANSIT = 1
    DELIVERED = 2

    ORDER_STATUS = (
        (ORDERED, "ordered"),
        (IN_TRANSIT, "In transit"),
        (DELIVERED, "Delivered"),
    )
    order_status = models.SmallIntegerField(choices=ORDER_STATUS, default=ORDERED)  # Define um campo de inteiro pequeno com opções de status de pedido
    tracking_number = models.CharField(max_length=50)  # Define um campo de caractere para o número de rastreamento
    user = models.ForeignKey(
        AppUser,  # Define um campo de chave estrangeira para o modelo AppUser
        related_name='orders', null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name='User')

    address = models.ForeignKey(Address, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='Address')  # Define um campo de chave estrangeira para o modelo Address
    objects = OrderManager()  # Atribui o gerenciador de objetos OrderManager ao modelo

# Define um novo modelo chamado OrderItem que herda de TimestampedModel
class OrderItem(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='orders_is_in')  # Define um campo de chave estrangeira para o modelo Product
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False, related_name='order_items')  # Define um campo de chave estrangeira para o modelo Order
    quantity = models.IntegerField(validators=[MinValueValidator(1)])  # Define um campo de inteiro para a quantidade com um validador de valor mínimo
    name = models.CharField(max_length=50)  # Define um campo de caractere para o nome do item
    slug = models.CharField(max_length=50)  # Define um campo de caractere para o slug do item
    price = models.FloatField(validators=[MinValueValidator(1.0)])  # Define um campo de ponto flutuante para o preço com um validador de valor mínimo
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True, related_name='products_bought')  # Define um campo de chave estrangeira para o modelo AppUser
    # user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, related_name='order_items')
